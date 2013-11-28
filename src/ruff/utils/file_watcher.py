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
import os
import time


class FileWatcher(object):
  """ Watches for file changes.

      The callback handles file matching; it is invoked on
      all paths which are 'new' since the last call until it
      return True.

      So, to process all new files, always return False.
      To halt after the first match, return True.

      Typical usage:

      def process_file(path, observer):
        if re.match(".*\.py", path):
          ... # Do things
          return True

      observer = FileWatcher('.', action=process_file)
      while True:
        observer.poll()
        time.sleep(1)
  """

  def __init__(self, path=os.getcwd(), since=0, action=None, recursive=True):
    self.path = path
    self.since = since
    self.action = action
    self.recursive = recursive

  def _updates(self):
    """ Yield files that are update/new until action accepts one """
    for root,dirs,files in os.walk(self.path):
      for filename in files:
        path = os.path.join(root, filename)
        stats = os.stat(path)
        if stats.st_mtime > self.since or stats.st_ctime > self.since:
          yield path

  def run(self):
    updated = False
    for path in  self._updates():
      if self.action is not None:
        if self.action(path, self):
            updated = True
            break
    if updated:
        self.since = time.time()
    return updated
