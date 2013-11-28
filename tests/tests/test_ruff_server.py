import sys
import os
import unittest
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import ruff


class Test(object):
    def __init__(self):
        self.delta = 0
        self.state = 0

    def callback(self, context, elapsed_time):
        self.delta += elapsed_time
        if self.delta > 1.0 and self.state == 0:
          try:
            content = requests.get('http://localhost:50009/helpers.py')
            assert content.text is not None
            self.state = 1
          except Exception as e:
            self.state = 2
        elif self.delta > 2.0:
          return False
        return True


class TestRunner(unittest.TestCase):
    def test_ruff(self):
        ruff.reset()
        test = Test()
        ruff.serve('localhost', 50009, ruff.path('.'))
        ruff.run(__file__, callback=test.callback)
        assert test.state == 1


if __name__ == '__main__':
    unittest.main()
