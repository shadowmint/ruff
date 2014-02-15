from __future__ import absolute_import
import os
import re
from ruff.state import State
from ruff.utils.run import run
from ruff.os import WINDOWS, Color


class Build(object):
  """ Keeps track of a build order """

  def __init__(self):
    self._orders = []

  def execute(self):
    """ Run all the orders in this builder """
    for order in self._orders:
      try:
        if order['type'] == 'command':
          print('- {0}Executing custom operation{1}: {2}'.format(Color.GREEN, Color.RESET, order['command']))
          order['command'](State.instance.path)
        elif order['type'] == 'chdir':
          print('- {0}Moving to folder{1}: {2}'.format(Color.BLUE, Color.RESET, order['path']))
          os.chdir(order['path'])
        elif order['type'] == 'run':
          self._run(*order['command'])
        elif order['type'] == 'collection':
          print('- {0}Executing collection command{1}: {2}'.format(Color.GREEN, Color.RESET, order['command']))
          self._collect(order['pattern'], order['command'], order['recurse'])
      except Exception as e:
        self._report_error(e)
        print('- {0}Halting build for this sequence{1}'.format(Color.YELLOW, Color.RESET))

  def _report_error(self, error=None, message=None):
    """ Report an error message """
    if error is not None:
      print('- {0}Failed{1}: {2}'.format(Color.RED, Color.RESET, error))
    else:
      print('- {0}Failed{1}:'.format(Color.RED, Color.RESET))
    if message is not None:
      print(message)

  def run(self, *largs):
    """ Run a command on build """
    self._orders.append({'type': 'run', 'command': largs})
    return self

  def command(self, command):
    """ Add a callback command to be invoked on build """
    self._orders.append({'type': 'command', 'command': command})
    return self

  def chdir(self, path):
    """ Move to the given path """
    self._orders.append({'type': 'chdir', 'path': path})
    return self

  def collect(self, pattern, command, recurse=False):
    """ Add a callback command to be invoked on a collection """
    self._orders.append({'type': 'collection', 'pattern': pattern, 'command': command, 'recurse': recurse})
    return self

  def _run(self, *kargs):
    """ Safe runner """
    info = ' '.join(kargs)
    print('- {0}Executing{1}: {2}'.format(Color.GREEN, Color.RESET, info))
    success, output = run(*kargs, shell=WINDOWS, capture_output=True)
    if not success:
      self._report_error(message=output)
    else:
      print(output)

  def _collect(self, pattern, collector, recurse):
    """ Invoke the collector. It should be in the form:

        def collector(matches, run):
          for m in matches:
            run('...', '...', m)
    """
    collector(self._collect_files(pattern, recurse), self._run)

  def _collect_files(self, pattern, recurse):
    """ Return a list of all files that match pattern.
        :param pattern: A regex to match against
        :param recurse: If true, do this recursively
    """
    root = os.getcwd()
    matcher = re.compile(pattern)
    if recurse:
      for root, dirs, files in os.walk(root):
        for filename in files:
          path = os.path.join(root, filename)
          if matcher.match(path):
            yield path
    else:
      for filename in os.listdir(root):
        path = os.path.join(root, filename)
        if matcher.match(path):
          yield path
