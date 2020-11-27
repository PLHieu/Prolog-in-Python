import Fact

class Rule:
   def __init__(self, conclusion=Fact(), conditions=[]):
      self.conclusion = conclusion        # inferred fact
      self.conditions = conditions            # conditions: list of facts


   @staticmethod
   def parse_rule(rule_str):
      # Example: daughter(Person, Parent) :- female(Person), parent(Parent, Person).
      rule_str = rule_str.strip().rstrip('.').replace(' ', '')
      sep_idx = rule_str.find(':-')

      # Get conclusion (lhs) and premises (rhs) seperated by ':-'
      conclusion = Fact(rule_str[: sep_idx])
      conditions = []
      list_fact_str = rule_str[sep_idx + 2:].split('),')

      for idx, fact_str in enumerate(list_fact_str):
         if idx != len(list_fact_str) - 1:
            fact_str += ')'
         conditions.append(Fact(fact_str))
      return Rule(conclusion,conditions)

   def copy(self):
      return Rule(self.conclusion.copy(), self.condition.copy())

   def get_num_premises(self):
      return len(self.conditions)

   def get_ops(self):
      ops = set()
      for premise in self.conditions:
         ops.add(premise.op)
      return ops

   def helpful(self, fact_op):
      return fact_op in self.ops



