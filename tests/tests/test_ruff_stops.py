import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import ruff


class Test(object):
    def __init__(self):
        self.delta = 0

    def callback(self, context, elapsed_time):
        self.delta += elapsed_time
        if self.delta > 1.0:
            return False
        return True


class TestRunner(unittest.TestCase):
    def test_ruff(self):
        test = Test()
        ruff.run(__file__, callback=test.callback)


if __name__ == '__main__':
    unittest.main()
