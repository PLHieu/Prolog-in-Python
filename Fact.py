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
        else:
            self.op=''
            self.args=[]

    def __hash__(self):
        return hash(str(self))

    def init2(self, op, args):  # todo : is positive
        self.op = op  # relation or function
        self.args = args  # varibles and constants


    def init1(self, str):

        # Example: female(princess_diana).
        str = str.strip().rstrip('.').replace(' ', '')
        sep_idx = str.index('(')
        # Op and args are separated by '('
        self.op = str[:sep_idx]
        self.args = str[sep_idx + 1: -1].split(',')

    def copy(self):
        return Fact(self.op,self.args.copy())


    def __repr__(self):
        return '{}({})'.format(self.op, ', '.join(self.args))

    def __lt__(self, rhs):
        if self.op != rhs.op:
            return self.op < rhs.op
        return self.args < rhs.args

    def __eq__(self, rhs):
        if self.op != rhs.op:
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

    def get_args(self):
        return self.args

    def get_op(self):
        return self.op


