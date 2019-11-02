from parser33 import parser
from ast import data_dict
from lexer import lexer
from pprint import *

#code = '1+1 \\n 10-2'
#code = ' let x = 1 \\n x * 3'

#code = '1 + 1 \\n 2 + 2 \\n 3 + 3'

code = 'let x = 2.5 \\n let y = -10 \\n x / 5 \\n x * y'   # [None, None, 0.5, -25])

result = parser.parse(lexer.lex(code)).eval()
print(result)
pprint(data_dict)
