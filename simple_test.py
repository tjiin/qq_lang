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

# code1 = '-10 * -9'
# code1 = '10 * -9'
# code1 = '-10*-9'
# code1 = '----(3)'

'''code1 = """
        function parent(a){
            a = a * 10
            function child(b){
                b = b + 1
                return(b)
            }
        return(a + child(a))
        }
        """'''

code1 = "function test(a){ return(a+1) } ; function parent(b){ let c = b + test(b) \\n return(c) } ; parent(2)"
# code1 = "function test(a){ return(a+1) } ; test(10) ; 1+1 ; 5 > -5"
# code3 = "parent(2)"

program = Compile(code1)
space = program.namespace
"""program.print_full()
program = Compile(code2, space=space)
program.print_full()
program = Compile(code3, space=space)
program.print_full()"""


"""print('-'*50)
program = Compile(code2, space=space)
program.print_full()"""


