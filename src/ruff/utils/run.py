from __future__ import absolute_import
import os
import subprocess


def run(program, *kargs, **kwargs):
  """ Run a program on the path, with arguments.

      Use it like this:

      run("ls", "/home/")

      Or, if you just want to check IF the command can run,
      without actually running it, pass 'check_only' like this:

      run("ls", check_only=True)

      To capture the output of the command (including errors)
      use:

      success, output = run("ls", "/bin", capture_output=True)

      Finally, if you want to use a custom set of search paths
      (eg. in a virtualenv) instead of the common ones, use:

      run("python", "blah.py", PATH=["/bin", "/usr/bin", "/local/venv"])
  """
  check_only = kwargs.get("check_only", False)
  capture_output = kwargs.get("capture_output", False)
  path = kwargs.get("PATH", os.environ["PATH"].split(os.pathsep))
  shell = kwargs.get("shell", False)
  rtn = True
  resolved = which(program, path)
  if check_only:
    rtn = resolved is not None
  else:
    if resolved is not None:
      prog = [resolved]
      prog.extend(kargs)
      if capture_output:
        try:
          output = subprocess.check_output(prog, stderr=subprocess.STDOUT, shell=shell)

          # python3 likes to use byte strings; try to force to str
          for i in ['utf8', 'cp1252']:
            try:
              output = output.decode(i)
              break
            except:
              pass

          rtn = True, output
        except subprocess.CalledProcessError as e:
          rtn = False, e.output
      else:
        try:
          subprocess.call(prog, shell=shell)
        except subprocess.CalledProcessError:
          rtn = False
    else:
      raise BadCommandException("Missing command: '%s'" % program)
  return rtn


def is_exe(fpath):
  """ Check file exists and is executable.
      TODO: Better way to do this maybe?
  """
  return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(program, paths):
  """ Resolve a program from the PATH if possible """
  fpath, fname = os.path.split(program)
  if fpath and is_exe(program):
    return program
  else:
    for path in paths:
      path = path.strip('"')
      exe_file = os.path.join(path, program)
      if is_exe(exe_file):
        return exe_file
      elif is_exe(exe_file + ".exe"):
        return exe_file + ".exe"
  return None


class CommandLine(object):
  """ For generating long sequences of command line arguments.
  """

  def __init__(self):
    self.__values = []

  def run(self, *kargs):
    cmd = ' '.join(kargs)
    self.__values.append(cmd)

  def __str__(self):
    """ Use this only in shells that make sense """
    rtn = '\n'.join(self.__values)
    rtn = rtn.replace("c:", "/c")
    rtn = rtn.replace("\\", "/")
    return rtn


class BadCommandException(Exception):
  pass

