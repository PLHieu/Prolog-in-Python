
from Fact import Fact

class Rule:
       # conditions: list of facts

   #todo ham can thiet thay vi getter setter
   def __init__(self, *inp):
       if (len(inp) == 1):
          self.init1(inp[0])
       else:
          self.init2(inp[0], inp[1])


   def init1(self,rule_str):
      # Example: daughter(Person, Parent) :- female(Person), parent(Parent, Person).
      rule_str = rule_str.strip().rstrip('.').replace(' ', '')
      sep_idx = rule_str.find(':-')

      # Get conclusion (lhs) and premises (rhs) seperated by ':-'
      self.conclusion = Fact(rule_str[: sep_idx])
      self.conditions = []
      list_fact_str = rule_str[sep_idx + 2:].split('),')

      for idx, fact_str in enumerate(list_fact_str):
         if idx != len(list_fact_str) - 1:
            fact_str += ')'
         self.conditions.append(Fact(fact_str))

   def init2(self, conclusion=Fact(), conditions=[]):
      self.conclusion = conclusion  # inferred fact
      self.conditions = conditions


   def copy(self):
      return Rule(self.conclusion.copy(), self.condition.copy())

   def get_num_premises(self):
      return len(self.conditions)

   def get_ops(self):
      ops = set()
      for condition in self.conditions:
         ops.add(condition.op)
      return ops

   def helpful(self, fact_op):
      return fact_op in self.ops



