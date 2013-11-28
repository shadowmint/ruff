class Binding(object):
  """ A target - action binding """

  def __init__(self, target):
    """ Create a binding """
    self.target = target
    self.builders = []
    self.matched = False
    self.target.parent = self

  def build(self, builder):
    self.builders.append(builder)

  def run(self):
    """ Run the build actions attached to this observer """
    if self.matched:
      for b in self.builders:
        b.execute()
      return True

  def check(self):
    """ Check if we need to run this binding """
    self.matched = False
    for observer in self.target.observers:
      observer.run()

  def register(self):
    """ Child observers may call this """
    self.matched = True
