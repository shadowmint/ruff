from ruff.utils._os import platform, platforms


# Easy to use os constants
WINDOWS = platform() == platforms.WINDOWS
MAC = platform() == platforms.MAC
UNIX = platform() == platforms.LINUX


if WINDOWS:
  class Color(object):
    WHITE = ''
    BLUE = ''
    GREEN = ''
    YELLOW = ''
    RED = ''
    RESET = ''
else:
  class Color(object):
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
