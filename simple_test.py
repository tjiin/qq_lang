from parser33 import parser
from ast import data_dict
from lexer import lexer
from pprint import *

code = '1+1 \\n 10-2'
#code = ' let x = 1 \\n x * 3'
"""tokens = lexer.lex(code)
print(tokens)
for t in tokens:
    print(t)
"""
result = parser.parse(lexer.lex(code)).eval()
print(result)
pprint(data_dict)
