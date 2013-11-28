def singleton(cls):
  """ Provides a simple singleton provider.

      For more complicated situations, it's probably better to use
      resolve() to resolve a scope for an entire class, but for simple
      uses, @singleton can be used as so:

      @singleton
      class MyType(object):
        def __init__(self):  # Notice the null constructor
          ...

      singleton = MyType.instance

      Attempting to create an instance using MyType() will result in a
      SingleInstanceError.
  """
  def fake_init(self):
    raise SingleInstanceError(cls)
  if not hasattr(cls, 'instance'):
    cls.instance = cls()
    cls.__init__ = fake_init
  return cls


class SingleInstanceError(Exception):
  def __init__(self, cls):
    msg = "Invalid attempt to create instance of singleton '%s' (use %s.instance)" % (cls.__name__, cls.__name__)
    super(SingleInstanceError, self).__init__(msg)
