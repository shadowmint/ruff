from __future__ import absolute_import
import os
import time
from os.path import abspath, dirname, join
from ruff.utils.singleton import singleton
from ruff.utils.fn import unique
from ruff.build import Build
from ruff.target import Target
from ruff.binding import Binding
from ruff.state import State
from ruff.service import run_server, run_command


def reset():
  """ Reinitialize state """
  State.instance.clear()


def path(path, *largs):
  """ Convert *largs into a path relative to the file path.
      :param string path: The path to a file, eg. from __file__
      :param largs: The arguments to bind into the path.
  """
  segments = [dirname(path)]
  if len(largs):
    segments.extend(largs)
  return abspath(join(*segments))


def run(path=None, callback=None, poll=0.1):
  """ Poll for file changes periodically and run on the path of the given file
      :param string path: The path to a file, eg. from __file__
      :param lambda callback: A callback to invoke every round
      :param float poll: The callback interval.
  """
  if path is None:
    path = os.getcwd()

  # run commands
  for record in State.instance.commands:
    pid = run_command(*record)
    State.instance.command_pids.append(pid)

  # run servers
  for record in State.instance.servers:
    pid = run_server(*record)
    State.instance.server_pids.append(pid)

  # run local
  context = abspath(dirname(path))
  State.instance.path = context
  while True:
    try:
      ran = False
      for binding in State.instance.bindings:
        binding.check()
      for binding in State.instance.bindings:
        victory = binding.run()
        if victory:
          ran = True
      if ran:
        print('- Done')
      time.sleep(poll)
      if callback:
        if not callback(context, poll):
          break
    except Exception as e:
      pass

  # halt servers and commands
  for pid in State.instance.server_pids:
    pid.terminate()
  for pid in State.instance.command_pids:
    pid.terminate()


def bind(target, *largs):
  """ Attach a binding
      :param Target target: The target for this binding.
      :param largs: The set of builders to invoke on this target.
  """
  binding = Binding(target)
  for l in largs:
    binding.build(l)
  target.parent = binding
  State.instance.bindings.append(binding)


def build():
  """ Return a new builder """
  return Build()


def target(timeout=0):
  """ Return a new target
      :param float timeout: Maximum timeout for this target.
  """
  return Target(timeout)


def serve(host, port, folder):
  """ Setup a local webserver for testing runnong on the given host,port,folder
      Note that the server won't actually start until run is called.
      :param string host: ...
      :param int port: ...
      :param string folder: ...
  """
  s = State.instance
  s.servers.append((host, port, folder))


def command(*largs):
  """ Setup a local command to run in a subprocess """
  s = State.instance
  s.commands.append(largs)
