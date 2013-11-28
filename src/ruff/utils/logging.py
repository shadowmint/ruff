# Copyright 2013 Douglas Linder
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
import logging
import traceback


# Default format for error messages
DEFAULT_ERROR_FORMAT = '%(name)s: %(message)s (%(levelname)s)'


class ErrorHandlerBase(logging.StreamHandler):
  """ Base for custom handlers """

  def publish(self, msg):
    self.stream.write(msg)
    self.stream.write('\n')

  def emit(self, record):
    msg = self.format(record)
    self.publish(msg)
    if not Logging._suppress_exceptions:
      try:
        msg = traceback.format_exc()
        if msg is not None and str(msg) != "None\n":
          self.publish(msg)
      except AttributeError:
        pass  # Fails in py3


class ErrorTracebackHandler(ErrorHandlerBase):
  """ Default error handler """

  def publish(self, msg):
    self.stream.write(msg + '\n')


class LContiner(object):
  """ Looks after log handlers properly """

  def __init__(self, name):
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.DEBUG)
    self._handlers = []

  def add_handler(self, handler):
    self.logger.addHandler(handler)
    self._handlers.append(handler)

  def clear(self):
    for h in self._handlers:
      self.logger.removeHandler(h)


class Logging(object):
  """ Convenience helper to get a named logger """

  # Default format for log messages
  _format = DEFAULT_ERROR_FORMAT

  # Default logger
  _handler = ErrorTracebackHandler

  # Should exceptions be supressed?
  _suppress_exceptions = False

  # The output level
  _level = logging.DEBUG

  # Active loggers
  __loggers = {}

  @classmethod
  def suppress_exceptions(cls, value=True):
    """ Suppress annoying exceptions when not interested """
    cls._suppress_exceptions = value

  @classmethod
  def _logger(cls, name):
    if name not in cls.__loggers:
      cls.__loggers[name] = LContiner(name)
      handler = cls._handler()
      formatter = logging.Formatter(cls._format)
      handler.setFormatter(formatter)
      handler.setLevel(cls._level)
      cls.__loggers[name].add_handler(handler)
    return cls.__loggers[name]

  @classmethod
  def level(cls, level=logging.DEBUG):
    self._level = level

  @classmethod
  def handler(cls, new_handler=None):
    if new_handler is None:
      cls._handler = ErrorTracebackHandler
    else:
      cls._handler = new_handler
      cls.reset()

  @classmethod
  def format(cls, new_format):
    cls._format = new_format

  @classmethod
  def get(cls, depth=1):
    import inspect

    frame = inspect.stack()[depth]
    target = frame[1]
    return cls._logger(target).logger

  @classmethod
  def reset(cls):
    """ Reset the handlers """
    for name in cls.__loggers:
      cls.__loggers[name].clear()
    cls.__loggers = {}
