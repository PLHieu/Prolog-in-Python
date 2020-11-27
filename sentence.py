def categorizeofsentence(str):
   sent_str = str.strip()
   if not sent_str:
      return 'space'
   if ':-' in sent_str:
      return 'rule'
   if sent_str.startswith('/*') and sent_str.endswith('*/'):
      return 'comment'
   return 'fact'

def getnextquery(inp_str):
   next_sentence = inp_str[i].strip()
   i = 0
   if not next_sentence.startswith('/*'):
      while not next_sentence.endswith('.'):
         i += 1
         next_sentence += inp_str[i].strip()
   elif next_sentence:
      while not next_sentence.endswith('*/'):
         i += 1
         next_sentence += inp_str[i].strip()
#return next sentence and remain string
   return next_sentence, inp_str[i + 1:]
