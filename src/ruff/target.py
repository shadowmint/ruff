from ruff.utils.fn import unique
from ruff.utils.file_watcher import FileWatcher
import re


class Target(object):
    """ Keeps track of a specific type of target """

    def __init__(self, timeout):
        self.observers = []
        self.parent = None
        self.timeout = timeout

    def pattern(self, regex, folder, recurse=False):
        """ Add a pattern to the set current tracked here
            :param string regex: The regex to match files names against.
            :param string folder: The folder to match files in.
            :param string recurse: Should the directory free be recursed?
        """
        observer = FileWatcher(folder, recursive=recurse, action=self.action)
        observer.regex = regex
        self.observers.append(observer)

    def action(self, path, observer):
        if re.match(observer.regex, path):
            self.parent.register()
            print('- Matching build target: {0}'.format(path))
            return True

