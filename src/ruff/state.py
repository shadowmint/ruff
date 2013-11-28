from ruff.utils.singleton import singleton


@singleton
class State(object):
    """ Internal module state object """

    def __init__(self):
        self.bindings = []
        self.path = None
        self.servers = []
        self.server_pids = []
        self.commands = []
        self.command_pids = []

    def clear(self):
        """ Clear the held set of patter / builder bindings """
        self.bindings = []
        self.path = None
        self.servers = []
        self.server_pids = []
        self.commands = []
        self.command_pids = []

    @property
    def observers(self):
        """ Yield a list of observers """
        for binding in self.bindings:
            yield binding.observer
