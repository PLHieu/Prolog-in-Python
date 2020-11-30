from object import Fact
from object.Fact import *
def isUpper(pre):
    if (pre[0].isupper()):
        return True
    return False

def isLower(string):
    if (string[0].islower()):
        return True
    return False

def cacuElementUppercase(l):
    list_index_var = []
    n = len(l)
    for i in range(0,n):
        if isUpper(l[i]):
            list_index_var.append(i)

    return list_index_var

def categorizeofsentence(str):
   sent_str = str.strip()
   if not sent_str:
      return 'space'
   if ':-' in sent_str:
      return 'rule'
   if sent_str.startswith('/*') and sent_str.endswith('*/'):
      return 'comment'
   return 'fact'

def getnextquery(inp_str):
   i = 0
   next_sentence = inp_str[i].strip()
   if next_sentence.startswith('/*'):  # Comments
      while not next_sentence.endswith('*/'):
         i += 1
         next_sentence += inp_str[i].strip()
   elif next_sentence:  # Queries
      while not next_sentence.endswith('.'):
         i += 1
         next_sentence += inp_str[i].strip()
   return next_sentence, inp_str[i + 1:]

def is_variable(x):
   return isinstance(x, str) and x[0].isupper()

def is_compound(x):
   return isinstance(x, Fact)

def is_list(x):
   return isinstance(x, list)