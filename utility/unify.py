from object.Fact import *
from utility.utils import is_compound,is_variable,is_list
def is_variable(x):
   return isinstance(x, str) and x[0].isupper()

def is_compound(x):
   return isinstance(x, Fact)

def is_list(x):
   return isinstance(x, list)

def unify(x, y, theta):
   if theta is False:
      return False
   if x == y:        # i.e: Parent = Parent, z = z, Mary = Mary
      # everything
      return theta
   if is_variable(x):
      #have variable
      return unify_var(x, y, theta)
   if is_variable(y):
      return unify_var(y, x, theta)
   if is_compound(x) and is_compound(y):
      return unify(x.args, y.args, unify(x.op, y.op, theta))
   if is_list(x) and is_list(y) and len(x) == len(y):
      #unify each of list
      return unify(x[1:], y[1:], unify(x[0], y[0], theta))
   return False

def unify_var(var, x, theta):
   if theta.get_const(var):
      #get value of var in theta
      return unify(theta.get_const(var), x, theta)
   if theta.get_const(x):
      # get key of x in theta
      return unify(var, theta.get_const(x), theta)
   #x or var 's not in theta => add(key = var,value = x)
   theta.add(var, x)
   return theta

