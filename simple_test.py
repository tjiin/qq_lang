from parser33 import parser
from ast import data_dict
from lexer import lexer
from pprint import *

# code = '1+1 \\n 10-2'
# code = ' let x = 1 \\n x * 3'
# code = '1 + 1 \\n 2 + 2 \\n 3 + 3'
# code = r' let x = 10 + 9 \n let y = -10 \n x / 5 \n x * y'   # [None, None, 3.8, -190])

#code = r' let x = 18 \n print((x+1)*10, x) '
#code = r' print(10, 11, 12*-10) '
code = r' test(x,y,z)'

result = parser.parse(lexer.lex(code)).eval()
print(result)
pprint(data_dict)