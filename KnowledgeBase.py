import sentence
#import Sentence
import Fact

import Rule

class KnowledgeBase:
   def __init__(self,list_sentence):
      while list_sentence:
         sent_str, list_sentence = nextsentence(list_sent_str)
         sent_type = categorizeof(sent_str)
         if sent_type == 'fact':
            fact = Fact.parse_fact(sent_str)
            self.fact.append(fact)
         elif sent_type == 'rule':
            rule = Rule(sent_str)
            self.fact.append(rule)
