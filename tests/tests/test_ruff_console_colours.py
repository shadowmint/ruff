import sys
import os
import unittest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'src'))
import ruff
import helpers as h


class TestRunner(unittest.TestCase):
    def test_ruff_pass_colours(self):

        def command(*args):
          pass

        build = ruff.build()
        build.run('ls')
        build.chdir('.')
        build.command(command)
        build.collect("*", command)
        build.execute()

    def test_ruff_fail_command_colours(self):
        build = ruff.build()
        build.run('dfadf')
        build.execute()

    def test_ruff_fail_command_colours_for_return_code(self):
        build = ruff.build()
        build.run('ls', '--staticdafsfaf')
        build.execute()

    def test_ruff_fail_command_colours_for_chdir(self):
        build = ruff.build()
        build.chdir('/dafadsf/asdf/adsf/asdf/asdf')
        build.execute()

    def test_ruff_fail_command_colours_for_command(self):
        def command(p):
            raise Exception('No')
        build = ruff.build()
        build.command(command)
        build.execute()

    def test_ruff_fail_command_colours_for_collective(self):
        def command(p, run):
          for path in p:
            if not str(path).endswith('.py'):
              raise Exception('No: ' + str(path))
        build = ruff.build()
        build.collect('.*', command)
        build.execute()

if __name__ == '__main__':
    unittest.main()
