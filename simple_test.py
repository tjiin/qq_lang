from parser33 import Compile
from pprint import *

# code = '1 + 1'
# code = '1+1 \\n 10-2'
# code = ' let x = 1 \\n x * 3'
# code = '1 + 1 \\n 2 + 2 \\n 3 + 3'
# code = r' let x = 10 + 9 \n let y = -10 \n x / 5 \n x * y'   # [None, None, 3.8, -190])

# code = r' let x = 18 \n print((x+1)*10, x) '
# code = r' print(10, 11, 12*-10) '
# code = r' test(x,y,z)'

# code1 = r' function test(a) { a = 10 \n return(a * 10 + a) } \n test(2) '
# code1 = r' function test(a) { a = a * 10 \n return(a + 2) } \n test(2) '
# code1 = r' function test(a) { let b = 10 \n return(b * 10 + a) } '
# code2 = r' test(5) '

# code1 = "function test(a){ return(a+1) } ; function parent(b){ let c = b + test(b) \\n return(c) } ; parent(2)"
# code1 = "1 + test()"
# code1 = "test() + 1"

# code1 = "function f(a){ return(a+1) } ; function g(a){ return(a*10) } ; 1 + f(g(1)-8)"
# code1 = "function f(a){ return(a+1) } ; function g(a){ return(a*10) } ; "
# code2 = "f(5) + 1 == 7 and g(1) > 9"
# code1 = "f(g()) + 1"
# code1 = "f() == True"
# code1 = "function test(a){ return(a+1) } ; test(10) ; 1+1 ; 5 > -5"

# code1 = r'function f(a,b){ let c = (a-1)*(b+1) \n return(c) } ; function g(x){ return(x+1) } ; f( g(1), 7 )'  FAILS
# code1 = r'function f(a,b){ let c = (a+1)/(b - 1) \n return(c) } ; function g(x){ return(x+1) } ; f( g(1), 7 )'
code1 = "1 -1"
code1 = 'let x = 10; x-1'

program = Compile(code1)
space = program.namespace
# print('-'*10)
# program = Compile(code2, space=space)