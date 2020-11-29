from checkarg import is_list,is_variable,is_compound
import copy
class Fact:
    def __deepcopy__(self, memodict={}):
        return Fact(self.op,copy.deepcopy(self.args))

    def __init__(self, *inp):
        if len(inp)== 1:
            self.init1(inp[0])
        elif len(inp)==2:
            self.init2(inp[0],inp[1])
        elif len(inp) == 3:
            self.init2(inp[0],inp[1], inp[2])



    def __hash__(self):
        return hash(str(self))

    def init2(self, op, args, negative = False):
        self.op = op
        self.args = args
        self.negative = negative

    def init1(self, str):

        # Example: female(princess_diana).
        str = str.strip().rstrip('.').replace(' ', '')
        sep_idx = str.index('(')
        # Op and args are separated by '('
        self.op = str[:sep_idx]
        # Neu nhu phia truoc co dau ~
        if '~' in self.op:
            self.op = self.op[1:]
            self.negative = True
        else:
            self.negative = False

        # parse Arguments
        self.args = str[sep_idx + 1: -1].split(',')
	
    def copy(self):
        return Fact(self.op,self.args.copy(), self.negative)

    def negate(self):
        self.negative = not self.negative

    def __repr__(self):
        if(self.negative):
            return '~{}({})'.format(self.op, ', '.join(self.args))
        else:
            return '{}({})'.format(self.op, ', '.join(self.args))

    def __lt__(self, rhs):
        if self.op != rhs.op:
            return self.op < rhs.op
        return self.args < rhs.args

    def __eq__(self, rhs):
        if self.op != rhs.op:
            return False
        if self.negative ^ rhs.negative:
            return False
        return self.args == rhs.args

    def contains_variable(self):
        for arg in self.args:
            if is_variable(arg):
                return True
        return False

    def contains_in_args(self,arg):
        for arg0 in self.args:
            if arg0==arg:
                return True
        return False

    @staticmethod
    def parse_fact(fact_str):

        fact_str = fact_str.strip().rstrip('.').replace(' ', '')
        sep_idx = fact_str.index('(')


        op = fact_str[:sep_idx]
        args = fact_str[sep_idx + 1: -1].split(',')
        return Fact(op, args)

    def update_predicate_string(self):
        """
        cap nhat lai string dai dien
        """
        self.predicate_string = '~'[not self.negative:] + self.op + '(' + ','.join(self.args) + ')'

    def unify_with_predicate(self, predicate):
        """
        dong nhat 2 fact trai dau, cung vitu voi nhau va cung so luong cac tham so
        tra ve false neu nhu khong dong nhat duoc, cung la bien, cung la hang o cac vi tri tuong ung, hoac khac do dai
        """
        if len(self.args) == len(predicate.args):
            substitution = {}
            return self.unify(self.args, predicate.args, substitution)
        else:
            return False

    def substitute(self, substitution):
        """
        substitution la mot dictionary anh xa may thay doi cua hang tu
        """
        if substitution:
            for index, arg in enumerate(self.args):
                if arg in substitution:
                    self.args[index] = substitution[arg]
            self.update_predicate_string()
        return self

    def unify(self, predicate1_arg, predicate2_arg, substitution):
        """
        dong nhat gia tri cua cac hang tu va tra ve mot dictionary anh xa
        tra ve False neu nhu khong anh xa duoc: cung la hang, cung la bien o 2 vi tri tuong ung
        """
        if substitution == False:
            return False
        elif predicate1_arg == predicate2_arg:
            return substitution
        elif isinstance(predicate1_arg, str) and predicate1_arg.islower():
            return self.unify_var(predicate1_arg, predicate2_arg, substitution)
        elif isinstance(predicate2_arg, str) and predicate2_arg.islower():
            return self.unify_var(predicate2_arg, predicate1_arg, substitution)
        elif isinstance(predicate1_arg, list) and isinstance(predicate2_arg, list):
            # neu ca 2 danh sach deu !rong
            if predicate1_arg and predicate2_arg:
                return self.unify(predicate1_arg[1:], predicate2_arg[1:],
                                  self.unify(predicate1_arg[0], predicate2_arg[0], substitution))
            else:
                return substitution
        else:
            return False

    def unify_var(self, var, x, substitution):
        if var in substitution:
            return self.unify(substitution[var], x, substitution)
        elif x in substitution:
            return self.unify(var, substitution[x], substitution)
        else:
            substitution[var] = x
            return substitution
