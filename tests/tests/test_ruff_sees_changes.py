import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import ruff
import helpers as h


class Test(object):
    """ Test ruff can see a change in *.c and run a build on it """

    def __init__(self):
        self.delta = 0
        self.state = 0
        self.built = 0

    def callback(self, context, dt):
        self.delta += dt
        if self.state == 0:
            h.touch_file(h.path('src', 'src5.c'))
            self.state = 1
        if self.delta > 0.5:
            h.touch_file(h.path('src', 'sub', 'src6.c'))
        if self.delta > 1.0:
            return False
        return True

    def active(self, context):
        self.built += 1


class TestRunner(unittest.TestCase):
    def test_ruff(self):
        test = Test()

        # Sources
        c_src_path = ruff.path(__file__, 'src')
        c_targets = ruff.target()
        c_targets.pattern('.*\.c', c_src_path, recurse=True)

        # Builds
        c_build = ruff.build()
        c_build.command(test.active)

        # Bind
        ruff.bind(c_targets, c_build)

        # Run
        ruff.run(__file__, callback=test.callback)
        assert test.built >= 2


if __name__ == '__main__':
    unittest.main()
