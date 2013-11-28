import multiprocessing
import os
from ruff.utils.run import run


def run_server(host, port, folder):
  print('server: %r %r %r' % (host, port, folder,))
  p = Server(folder, host, port)
  p.start()
  return p


def run_command(*largs):
  print('command: %r' % (largs,))
  p = Command(*largs)
  p.start()
  return p


class Server(multiprocessing.Process):
  """ Server~ """

  # Is flask is not available?
  DISABLED = False
  
  def __init__(self, folder, host, port):
    super(Server, self).__init__()
    self.folder = folder
    self.port = port
    self.host = host
    self._app = None

  @property
  def app(self):
    if self._app is None:
      from werkzeug import SharedDataMiddleware
      from flask import Flask
      app = Flask(__name__)
      app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {'/': self.folder})
      app.deubg = True
      self._app = app
    return self._app

  def run(self):
    try:
      has_deps = True
      try:
        from tornado.wsgi import WSGIContainer
        from tornado.httpserver import HTTPServer
        from tornado.ioloop import IOLoop
      except: 
        print('- !! Unable to run local server; missing dependency: tornado')
        has_deps = False
      try:
        from werkzeug import SharedDataMiddleware
        from flask import Flask
      except: 
        print('- !! Unable to run local server; missing dependency: flask')
        has_deps = False
      if not has_deps:
        return
      http_server = HTTPServer(WSGIContainer(self.app))
      http_server.listen(self.port)
      IOLoop.instance().start()
    except Exception as e:
      print('Failed to run flask server: {0}'.format(e))
      import traceback
      traceback.print_exc()
      os._exit(0)


class Command(multiprocessing.Process):
  """ Arbitrary command~ """

  def __init__(self, *largs):
    super(Command, self).__init__()
    self.args = largs

  def run(self):
    try:
      run(*self.args)
    except Exception as e:
      print('Failed to run command: {0}'.format(e))
      import traceback
      traceback.print_exc()
      os._exit(0)
