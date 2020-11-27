class Fact:
    def __init__(self, op='', args=[], negated=False):
        self.op = op  # relation or function
        self.args = args  # varibles and constants

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


    def copy(self):
        return Fact(self.op, self.args.copy())


    def get_args(self):
        return self.args

    def get_op(self):
        return self.op

    @staticmethod
    def parse_fact(str):
        # Example: female(princess_diana).
        str = str.strip().rstrip('.').replace(' ', '')
        sep_idx = str.index('(')

        # Op and args are separated by '('
        op = str[:sep_idx]
        args = str[sep_idx + 1: -1].split(',')
        return Fact(op, args)
