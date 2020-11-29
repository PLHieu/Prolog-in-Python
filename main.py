from object.KnowledgeBase import *
from object.Fact import *

def queryIntime():
   while(True):
      inp_file = input("Please Enter Knowledge Base file path: ")
      if (inp_file == "exit"):
         return False
      try:
         kb = KnowledgeBase(inp_file)
         while (True):
            print("?- ", end="")
            query_string = input("")
            if (query_string == "stop"):
               break
            type = input("Type of reasoning (1-Forward, 2-Backward, 3-Resolution): ")
            alpha = Fact(query_string)
            result = kb.query(alpha, int(type))
            print(result)
      except:
         print("There are some errors opening the the file, please try again")


def genOutputfile():
   inp_file = input("Please enter Knowledge Base file path: ")
   query_file = input("Please enter query file path: ")
   outp_file = input("Please enter output file path: ")
   type_reasoning = input("Please enter type reasoning (1-Forward, 2-Backward, 3-Resolution): ")
   try:
      kb = KnowledgeBase(inp_file)
      with open(query_file, 'r') as f_query:
         with open(outp_file, 'w') as f_out:
            for line in f_query.readlines():
               alpha = Fact(line)
               line = line + '.'
               theta_result = set(kb.query(alpha, int(type_reasoning)))
               substs_str = ' ;\n'.join([str(subst) for subst in theta_result]) + '.\n'
               f_out.write(line + '\n')
               f_out.write(substs_str + '\n')
   except:
      print("There are some errors, please try again")

if __name__ == '__main__':
   mode = input("Please select mode (1-Querying intime, 2-Generate result in output file): ")
   if int(mode) == 1:
      queryIntime()
   elif int(mode) == 2:
      genOutputfile()
