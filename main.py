# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import KnowledgeBase

inp_file = 'test/knowledgebase.pl'
query_file = 'test/query.pl'
outp_file = 'test/answers.txt'

def loadData():
    kb = KnowledgeBase()
    with open(inp_file, 'r') as f_in:
        list_sentences = f_in.readlines()
        print(list_sentences)
        KnowledgeBase.declare(kb, list_sentences)

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
