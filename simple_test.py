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

# code1 = r' def test(a) { a = 10 \n return(a * 10 + a) } \n test(2) '
# code1 = r' def test(a) { a = a * 10 \n return(a + 2) } \n test(2) '
# code1 = r' def test(a) { let b = 10 \n return(b * 10 + a) } '
# code2 = r' test(5) '

# code1 = "def test(a){ return(a+1) } ; def parent(b){ let c = b + test(b) \\n return(c) } ; parent(2)"
# code1 = "1 + test()"
# code1 = "test() + 1"

# code1 = "def f(a){ return(a+1) } ; def g(a){ return(a*10) } ; 1 + f(g(1)-8)"
# code1 = "def f(a){ return(a+1) } ; def g(a){ return(a*10) } ; "
# code2 = "f(5) + 1 == 7 and g(1) > 9"
# code1 = "f(g()) + 1"
# code1 = "f() == True"
# code1 = "def test(a){ return(a+1) } ; test(10) ; 1+1 ; 5 > -5"

# code1 = r'def f(a,b){ let c = (a-1)*(b+1) \n return(c) } ; def g(x){ return(x+1) } ; f( g(1), 7 )' # unexpected NEG
# code1 = r'def f(a,b){ let c = (a+1)/(b - 1) \n return(c) } ; def g(x){ return(x+1) } ; f( g(1), 7 )'
# code1 = "1 -1"
# code1 = 'let x = 10; x-

# code1 = ' f(x)=>{let a = x*10; return(a+x)};f(2)+f(-2)'

# code1 = ' def f(x){ def g(a){ let b = a / 2; return(a+b) } ; return( g(10) + x ) } ; f(1) '  # function defined in a function

# code1 = ' def f(x){ return(f(x)) } ; f(1) ' # Recursive, f is undefined in namespace f..

# code1 = 'f(x)=>{ let c = x + 1; return(c) } ; if( 0 < 5 ) then f(0)'
# code1 = "f(x)=>{let c=x+1; return(c)} ; if(0 < 5){let y = f(3A.5)*2 ; y=y+1 ; }"

# code1 = "if 1 < 0 then let x = -10 else let x = 10 "
# code1 = " let x = 5; if x < 0 then x = -10 else x = 10 "
# ode1 =  "let x = 5; if x > 0 then x = 10 elif x < 0 then x = -10  ; else x = 123"

code1 =  "let x = 5; if x > 0 then x = 10 elif x < 0 then x = -10"
# code1 = " let x = 0; if x > 0 then x = 10 elif x < 0 then x = -10 else x = 0 "

code1 = "let x = -1 ; if x > 0: x = 0"
code1 = "let x = 100 ; if x > 0: x = 0"
code1 = "let x = -1 ; if( x > 0 ){ x = 0 ; }"
code1 = "let x = 25.2 ; if( x > 0 ){ x = 0 ; }"
code1 = "let x = 25.2 ; if( x > 0 ): x = 0 "

code1 = "let x = 25.2 ; if x > 0 then x = 1 else x = -1"

code1 = "let x = -0.01 ; if x > 0 then x = 1 else x = -1"
code1 = "let x = -0.01 ; if x > 0: x = 1 else x = -1"
code1 = "let x = -0.01 ; if(x > 0): x = 1 else x = -1"

code1 = "let x = -10 ; if x > 0 then x = 1 elif x == 0 then x = 0 else x = -1"
code1 = "let x = -0 ; if x > 0 then x = 1 elif x == 0 then x = 0 else x = -1"
code1 = "let x = 25.2 ; if x > 0 then x = 1 elif x == 0 then x = 0 else x = -1"

code1 = "let x = -10 ; if x > 0 then x = 1 elif x < 0 then x = -1"
code1 = "let x = 0 ; if x > 0 then x = 1 elif x < 0 then x = -1"      # good test case
code1 = "let x = 25.2 ; if x > 0 then x = 1 elif x < 0 then x = -1"


code1 = "let x = 25.2 ; if x > 0 then x = 1 elif x == 0 then x = 0 else x = -1"

"""code1 = "let x=-10;if(x>0){x=1;}elif(x==0){x=0;}else{x=-1;}"
code1 = "let x=-10;if x>0{x=1;}elif x==0{x=0;}else{x=-1;}"


code1 = "f(a)=>{let c=0; if a<0:c=-1 else c=1; return(c)} ; f(0)"

code1 = "def g(x){ return(x/2) } ; let x = 15 ; let y = g(x) >= 10 ? 3 : -3"

code1 = "f(x)=>x+1 ; f(10)"

code1 = "2 > 5 ? 10 : -10"

code1 = r"let x = 2 > 5 ? 10 : -10"

code1 = "let a = 0; let b = a; " # let c = 2; a = b = 10;"

code1 = "let x = 10; while(x > 0){ x = x - 1; }; let y = x;"

code1 = "let x = 0; x++"""



# code1 = "let x = -0.01 ; if(x > 0){  x = 1 ; let y = x - 2 ; } else { x = -1 ; let y = x + 2 ; }"]]
# code1 = "let x = 0.01 ; if(x > 0){  x = 1 ; let y = x - 2 ; } else { x = -1 ; let y = x + 2 ; }"


program = Compile(code1)
space = program.namespace
print(space)
# print('-'*10)
# program = Compile(code2, space=space)