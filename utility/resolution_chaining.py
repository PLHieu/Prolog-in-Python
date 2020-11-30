from utility.utils import *
from object.CNF_Sentence import Statement
from object.Fact import Fact
# alpha la mot Fact
def resolution_chaining(kb,alpha):

    temp_kb =  set()

    # tao mot knowledge base moi chua cac statement o dang cnf
    # kb nay se o dang list cho de
    # Them cac facts
    for f in kb.facts:
        temp_kb.add(Statement(f,1))

    # Them cac rule o dang cnf
    for rule in kb.rules:
        temp_kb.add(Statement(rule,2))

    # init result list
    result = set()

    # Neu nhu la query dang yes/no question
    if not(haveElementUppercase(alpha.args)):
        alpha.negate()

        r = startloop(temp_kb, alpha)
        if r:
            result.add(True)

        return result

    # Neu nhu alpha o dang cau hoi Ai ? Caigi?
    else:
        # Thuc hien them vao temp_kb phu dinh tat ca cac truong hop co the cua alpha
        # Vi du: animal(X) thi them vao kb ~animal(ga), ~animal(heo)
        constant = kb.getConstants()

        # tim vi tri var trong args_alpha
        args_alpha = alpha.args
        i = 0
        for i in range(0, len(args_alpha)):
            if args_alpha[i].isupper():
                break

        for co in constant:
            temp_kb2 = copy.deepcopy(temp_kb)
            args_alpha_temp = copy.deepcopy(args_alpha)
            args_alpha_temp[i] = co
            new_fact = Fact(alpha.op, args_alpha_temp, True) #todo phu dinh alpha
            # alphaStatement = Statement(new_fact, 1)
            # alphaStatement.add_statement_to_KB(KB2, KB_HASH)
            # alphaStatement.add_statement_to_KB(temp_kb, KB_HASH)
            r = startloop(temp_kb2, new_fact)
            if r:
                result.add(co)

        return result

def startloop(temp_kb, new_fact, co = True):
    KB2 = set()
    KB_HASH = {}

    alphaStatement = Statement(new_fact, 1)
    alphaStatement.add_statement_to_KB(KB2, KB_HASH)
    alphaStatement.add_statement_to_KB(temp_kb, KB_HASH)

    while(len(temp_kb) < 200): #gioi han so phan tu co trong kb la 50

        history = {}
        new_statements = set()

        for statement1 in temp_kb:
            # lay danh sach tiem nang
            resolving_clauses = statement1.get_resolving_clauses(KB_HASH)
            for statement2 in resolving_clauses:
                if statement1 == statement2:
                    continue  # neu nhi gap lai chinh no thi continue
                flag1 = False
                flag2 = False
                if statement2.statement_string in history:
                    flag1 = True
                    if statement1.statement_string in history[statement2.statement_string]:
                        history[statement2.statement_string].discard(statement1.statement_string)
                        continue  #
                if statement1.statement_string in history:
                    flag2 = True
                    if statement2.statement_string in history[statement1.statement_string]:
                        history[statement1.statement_string].discard(statement2.statement_string)
                        continue  #
                # update history
                if flag2:
                    history[statement1.statement_string].add(statement2.statement_string)
                else:
                    history[statement1.statement_string] = set([statement2.statement_string])
                resolvents = statement1.resolve(statement2)  # hop giai statement1 voi statement2

                # neu nhu tra ve False tuc la 2 menh de doi ngau -> dpcm
                if resolvents == False:
                    # todo: chinh lai cho nay
                    # print(statement1, statement2, sep="***")
                    # return str(statement1)
                    # print(new_fact)
                    return True
                new_statements = new_statements.union(resolvents)
        if new_statements.issubset(temp_kb):
            return False
            # neu nhu kien thuc moi duoc sinh ra la tap con cuaa kb
            # -> kien thuc nay la hop ly
            # -> su ton tai cua ~alpha la hop li -> false
        new_statements = new_statements.difference(temp_kb)
        # update Knowledge base 2
        KB2 = set()
        KB_HASH = {}
        for stmt in new_statements:
            stmt.add_statement_to_KB(KB2, KB_HASH)

        temp_kb = temp_kb.union(new_statements)
