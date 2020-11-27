
from Fact import Fact
from sentence import getnextquery,categorizeofsentence
from Rule import Rule

class KnowledgeBase:
   #fact is list of condition

   def __init__(self):
      self.facts = set()
      self.rules = []

   def __init__(self, inp_file):
      self.facts = set()
      self.rules = []
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
