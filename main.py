from KnowledgeBase import KnowledgeBase
from Fact import Fact
inp_file = 'test/knowledge_base.pl'
query_file = 'test/query.pl'
outp_file = 'test/answers.txt'
from ClassTheta import Theta
from unify import unify



if __name__ == '__main__':
    kb = KnowledgeBase(inp_file)
    with open(query_file, 'r') as f_query:
       with open(outp_file, 'w') as f_out:
          for query_str in f_query.readlines():
             query = Fact(query_str)
             query_str = query_str + '.'
             theta_result = set(kb.query(query, 2))
             substs_str = ' ;\n'.join([str(subst) for subst in theta_result]) + '.\n'
             print(substs_str)
             f_out.write(query_str + '\n')
             f_out.write(substs_str + '\n')
