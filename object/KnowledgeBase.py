from object.Fact import Fact
from utility.utils import getnextquery,categorizeofsentence
from object.Rule import Rule
from utility.forward_chaining import forward_chaining
from utility.backward_chaining import backward_chaining
from utility.resolution_chaining import resolution_chaining
class KnowledgeBase:
   #fact is list of condition

   def __init__(self, facts, rules):
      self.facts = facts
      self.rules = rules


   def __init__(self, inp_file = None):
      self.facts = set()
      self.rules = []
      if inp_file:
         with open(inp_file, 'r') as f_in:
            list_sentences = f_in.readlines()

         while list_sentences:
            sent_str, list_sentences = getnextquery(list_sentences)
            sent_type = categorizeofsentence(sent_str)
            if sent_type == 'fact':
               self.facts.add(Fact(sent_str))
            elif sent_type == 'rule':
               rule = Rule(sent_str)
               self.rules.append(rule)

   def query(self, alpha, inference=1):
      if (inference == 1):
         return forward_chaining(self, alpha)
      elif (inference == 2):
         return backward_chaining(self, alpha)
      elif (inference ==3):
         return resolution_chaining(self,alpha)

   def getConstants(self):
      result = set()
      for fa in self.facts:
         for arg in fa.args:
            result.add(arg)
      return result

