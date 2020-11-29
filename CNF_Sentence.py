from Fact import *
import copy


class Statement():

    # def __init__(self, statement_string=None):
    #     if statement_string:
    #         predicate_list = statement_string.split('|')
    #         predicate_list = map(lambda x:Predicate(x), predicate_list)
    #         self.predicate_set = set(predicate_list)
    #         statement_string_list = map(lambda x: x.predicate_string, self.predicate_set)
    #         self.statement_string = '|'.join(statement_string_list)
    #     else:
    #         self.statement_string = None
    #         self.predicate_set = None

    # init from fact or rule
    def __init__(self, factRule=None, type=None):

        self.statement_string = ""
        self.predicate_set = set()

        if (factRule):
            if (type == 1):  # from fact
                self.predicate_set.add(factRule)
            elif (type == 2):  # from rule
                # trong rule luc nay dang chua dang & & =>
                # doi ve trai sang dang phu dinh, luc nay ta tu hien la ^
                # them gia thiet
                for predicate in factRule.conditions:
                    predicate.negate()
                    self.predicate_set.add(predicate)

                # them kl
                self.predicate_set.add(factRule.conclusion)

            # tien xu li statement


            self.updateStatementString()


        else:
            self.statement_string = None
            self.predicate_set = None

    def updateStatementString(self):
        # todo: xem lai phan nay de chuyen sang set
        n = len(self.predicate_set)
        i = 0
        for fact in self.predicate_set:
            if (i == n - 1):
                self.statement_string = self.statement_string + str(fact)
            else:
                self.statement_string = self.statement_string + str(fact) + " v "
            i = i + 1

    def init_from_string(self, statement_string):
        """
        """
        predicate_list = statement_string.split('|')
        predicate_list = map(lambda x: Fact(x), predicate_list)
        self.predicate_set = set(predicate_list)
        statement_string_list = map(lambda x: x.predicate_string, self.predicate_set)
        self.statement_string = '|'.join(statement_string_list)

    def init_from_predicate_set(self, predicate_set):
        """
        """
        self.predicate_set = predicate_set
        statement_string_list = map(lambda x: str(x), predicate_set)
        self.statement_string = '|'.join(statement_string_list)

    def __str__(self):
        return self.statement_string

    def __eq__(self, statement):
        return self.predicate_set == statement.predicate_set

    def __hash__(self):
        return hash((''.join(sorted(self.statement_string))))

    def exists_in_KB(self, KB):
        '''
        returns true if cnf_statement already exists
        in the KNOWLEDGE_BASE else False
        '''
        if self in KB:
            return True
        return False

    def add_statement_to_KB(self, KB, KB_HASH):
        """
        adds a statement in a knowledge base and updates the Hash
        """
        KB.add(self)
        for predicate in self.predicate_set:
            if predicate.op in KB_HASH:
                KB_HASH[predicate.op].add(self)
            else:
                KB_HASH[predicate.op] = set([self])

    def resolve(self, statement):
        '''
        hopgiai
        return false neu nhu phat hien menh de doi ngau -> dpcm
        return set cac kien thuc moi, set la {} neu nhu khong co kien thuc moi
        '''
        infered_statements = set()
        # lan luot ghep tung cap vi tu co trong 2 cau, neu nhu cap nao co cung ten va khac dau thi hop giai
        # sau khi hop giai tra kq ve unification
        # neu unification = False tuc la ..
        # unification la dictionary chua su thay doi cua cac bien -> hang
        # con khong thi
        for predicate_1 in self.predicate_set:
            for predicate_2 in statement.predicate_set:
                unification = False
                # neu nhu 2 fact la khac dau nhau va co cung vi tu
                if (predicate_1.negative ^ predicate_2.negative) and predicate_1.op == predicate_2.op:
                    unification = predicate_1.unify_with_predicate(
                        predicate_2)

                if (unification == False):
                    continue
                else:
                    rest_statement_1 = copy.deepcopy(self.predicate_set)
                    rest_statement_2 = copy.deepcopy(statement.predicate_set)
                    rest_statement_1 = list(filter(lambda x: False if x == predicate_1 else True, rest_statement_1))
                    rest_statement_2 = list(filter(lambda x: False if x == predicate_2 else True, rest_statement_2))
                    # neu nhu sau khi filter ma khong con ve nao trong cau thi do la 2 menh de doi ngau -> tra ve false -> tra ve True (dpcm)
                    if not rest_statement_1 and not rest_statement_2:  # contradiction found
                        return False
                    rest_statement_1 = list(map(lambda x: x.substitute(unification), rest_statement_1))
                    rest_statement_2 = list(map(lambda x: x.substitute(unification), rest_statement_2))
                    new_statement = Statement()
                    new_statement.init_from_predicate_set(set(rest_statement_1 + rest_statement_2))
                    infered_statements.add(new_statement)
        return infered_statements

    def get_resolving_clauses(self, KB_HASH):
        """
        returns a set of possible statements
        the self statement object can resolve with
        """
        resolving_clauses = set()
        for predicate in self.predicate_set:
            if predicate.op in KB_HASH:
                resolving_clauses = resolving_clauses.union(KB_HASH[predicate.op])
        return resolving_clauses

    def negate(self):
        # todo moi chi xu li cho mot Fact
        self.predicate_set