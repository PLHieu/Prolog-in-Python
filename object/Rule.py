from object.Fact import Fact
import random
import copy
class Rule:
       # conditions: list of facts

   #todo ham can thiet thay vi getter setter
   def __init__(self, *inp):
       if (len(inp) == 1):
          self.init1(inp[0])
       else:
          self.init2(inp[0], inp[1])
       self.conditions.sort()

   def __repr__(self):
      return '{} => {}'.format(' & '.join([str(cond) for cond in self.conditions]), str(self.conclusion))


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

   def __deepcopy__(self, memodict={}):
      return Rule(self.conclusion.copy(), copy.deepcopy(self.conditions))


   def init2(self, conclusion=Fact(), conditions=[]):
      self.conclusion = conclusion  # inferred fact
      self.conditions = conditions

   def is_potential_with(self, new_facts):
      for fact in new_facts:
         for condition in self.conditions:
            if (fact.op==condition.op):
               return True
      return False

   def copy(self):
      return Rule(self.conclusion.copy(), self.conditions.copy())

   def get_num_premises(self):
      return len(self.conditions)

   def change_variable_to(self,variable_name, new_variable_name):
      for idx in range(len(self.conclusion.args)):
         if self.conclusion.args[idx] == variable_name:
            self.conclusion.args[idx] = new_variable_name
      for condtion in self.conditions:
         for idx in range(len(condtion.args)):
            if condtion.args[idx] == variable_name:
               condtion.args[idx] = new_variable_name

   def generate_variable_name(self):
      i = random.randint(0, 1000)
      init_name = "X" + str(i)
      while self.contains_arg(init_name):
         init_name = init_name + str(i)
         i = i+1
      return init_name


   def contains_arg(self, arg):
      for condition in self.conditions:
         for arg0 in condition.args:
            if (arg0== arg):
               return True
      for arg0 in self.conclusion.args:
         if arg0 == arg:
            return True
      return False

   def get_ops(self):
      ops = set()
      for condition in self.conditions:
         ops.add(condition.op)
      return ops

   def contains_op(self, fact):
      for condition in self.conditions:
         if (condition.op == fact.op):
            return True
      if fact.op == self.conclusion.op:
         return True
      return False

#input is list facts
   def get_appropciate_fact(self, facts):
      approcitate_fact = []
      for fact in facts:
         if self.contains_op(fact):
            approcitate_fact.append(fact)
      return approcitate_fact
