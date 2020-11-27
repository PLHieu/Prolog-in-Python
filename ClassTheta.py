class Theta:
   def __init__(self):
      self.mappings = dict()

   def __repr__(self):
      return ', '.join('{} = {}'.format(key, value) for key, value in self.mappings.items())

   def __eq__(self, rhs):
      return self.mappings == rhs.mappings

   def __hash__(self):
      return hash(frozenset(self.mappings.items()))

   def empty(self):
      return len(self.mappings) == 0

   def get_const(self, var):
      if var in self.mappings:
         return self.mappings[var]


   def add(self, var, value):
      self.mappings[var] = value
