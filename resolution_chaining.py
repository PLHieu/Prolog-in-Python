
from CNF_Sentence import Statement

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

    KB2 = set()
    KB_HASH = {}
    # Them vao trong kb phu dinh cua alpha
    alpha.negate()
    alphaStatement = Statement(alpha,1)
    alphaStatement.add_statement_to_KB(KB2, KB_HASH)
    alphaStatement.add_statement_to_KB(temp_kb, KB_HASH)


    while(len(temp_kb) < 50): #gioi han so phan tu co trong kb la 50

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



def chuanhoa():
    pass
def doitenbiensangtenchuan():
    pass

def kiemtratapcon():
    pass

def resolutate(cau1, cau2):
    pass

def loaibotuongduong(cau):
    pass

def loaibosuyra(cau):
    pass

def chuyenandsangor(cau):
    pass

# kieu neu de x het thi khoong duoc nen chuyen sang aa,ab,ac
def doitenbiensangtenchuan(cau):
    pass
