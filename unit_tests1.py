from unittest import TestCase
from parser33 import Compile

two_arg_arithmetic = [
    ('add 2 pos', '1 + 1'), ('sub 2 pos', '8 - 4'), ('mul 2 pos', '4 * 8',), ('div 2 pos', '12 / 3'),
    ('add 2 neg', '-10 - 9'), ('sub 2 neg', '-1 - 41'), ('mul 2 neg', '-4 * -2',), ('div 2 neg', '-50 / -2'),
    ('pow 2 pos', '2**3'), ('pow 2 neg', '-2**-3')
]

compound_negatives = [
    ('double neg', '--2', 2), ('trip neg', '---2', -2), ('quad neg', '----2', 2),
    ('nested trip neg', '-(--(2))', -2), ('sub nested neg', '2--(-2)', 0),
    ('new line single neg var', 'let x = -1 \\n -x*2', [None, 2]),
    ('new line double neg var', 'let x = -1 \\n (--x)*2', [None, -2]),
    ('new line double neg var', 'let x = -1 \\n --x*2', [None, 2])
]

harder_arithmetic = [
    # Remember you can't use ^ for power if you're going to use python eval to check answer
    ('add sub 3 float', '2.5 - 99.65 + 0.001'), ('mul div 3 float', '2.5 * 99.65 / 0.001'),
    ('add/sub/mul/div nest paren neg', '((-0.1)+2.5)*(-99.65/(9-0.001))+((2.7))'),
    ('add/sub/mul/div OOP', '1 + 2 - 3 * 2 / 3 - 11'),
    ('add/sub/mul/div/pow OOP (1)', '3 - 3**2 * 2 + 10 + 2**3**-1'),
    ('add/sub/mul/div/pow OOP (2)', '(1+(2-3**3))*(3-2)'),
]

implicit_multiply = [
    ('implicit mul (0)(b)', '(0)(-1.7)', 0),
    ('implicit mul 0(b)', '0(-1.7)', 0),
    ('implicit mul (0)b', '(0)1.7', 0),
    ('not implicit mul (0)-b', '(0)-1.7', -1.7),
    ('implicit mul (a)(b)', '(-2.5)(-1.7)', 4.25),
    ('implicit mul a(b)', '-2.5(-0.65)', 1.625),
    ('implicit mul (a)b', '-0.1(-1.7)', 0.17),
    ('implicit mul ((a)(b))', '((-2)(2))', -4),
    ('implicit mul ((a)(b)(c))', '((2)(2)(2))', 8)
]

simple_and_or_not = [
    ('NOT no eval (1)', 'not True', False),
    ('NOT no eval (2)', 'not False', True),
    ('nested NOT no eval (1)', 'not(not(False))', False),
    ('nested NOT no eval (2)', 'not(not(True))', True),
    ('not True', 'not True', False),
    ('2 arg OR no eval (1)', 'False or False', False),
    ('2 arg OR no eval (2)', 'True or False', True),
    ('2 arg OR no eval (3)', 'False or True', True),
    ('2 arg OR no eval (4)', 'True or True', True),
    ('2 arg AND no eval (1)', 'False and False', False),
    ('2 arg AND no eval (2)', 'False and True', False),
    ('2 arg AND no eval (3)', 'True and False', False),
    ('2 arg AND no eval (4)', 'True and True', True),
    ('AND/OR/NOT no eval (1)', 'True and False or not False', True),
    ('AND/OR/NOT no eval (2)', 'True and False or not True', False),
    ('AND/OR/NOT expr (1)', 'True and (False or not False)', True),
    ('AND/OR/NOT expr (2)', 'False and True or False and True', False),
    ('AND/OR/NOT expr (3)', 'False or (True or False) and True', True)
]

equal_not_equal = [
    ('2 op EqualTo no eval (1)', '0 == 0', True),
    ('2 op EqualTo no eval (2)', '0 == 1', False),
    ('2 op EqualTo no eval (3)', '1 == 0', False),
    ('2 op NotEqualTo no eval', '0 != 0', False),
    ('2 op NotEqualTo no eval', '1 != 0', True),
    ('2 op NotEqualTo no eval', '0 != 1', True),
]

comparison = [
    ('2 op LessThan no eval (1)', '0 < 1', True),
    ('2 op LessThan no eval (2)', '1 > 0', True),
    ('2 op LessThan no eval (3)', '0 > 1', False),
    ('2 op LessThan no eval (4)', '1 < 0', False),
    ('2 op LessThanEqual no eval (1)', '2 <= 2', True),
    ('2 op LessThanEqual no eval (2)', '2 <= 1', False),
]

simple_var_assign = [
    ('var assign int', 'let x = 19', 'x', 19),
    ('var assign neg int', 'let x = -19', 'x', -19),
    ('var assign expr', 'let x = 19+(2*42/(-0.125))', 'x', -653),
]

new_line_expr = [
    ('2 line add/sub', r'1+1 \n 10-2', [2, 8]),
    ('2 line add/sub/mul/div', r' 2(-9.18/0.02) + 17 \n 1/2*(10-(-5)) ', [-901, 7.5]),
    ('3 line arithmetic', r'-3*3 \n 84/2 \n 9+8-6*5', [-9, 42, -13]),
]

new_line_var = [
    ('2 line assign eval', r'let x = 10 \n x + 1', 'x', 11),
    ('2 line neg assign eval', r'let x = -10 \n -x * -10', 'x', -100),
]

multi_line_vars = [
    ('3 line 3 var assign/eval', r'let x = 10 \n let y = -1.5 \n let z = x * y + 3', 'z', -12.0)
]

basic_functions = [
    ('func no arg no body return', r'def f(){ return(1+1) } \n f()', [None, 2]),
    ('1 line func no arg no body return', r'def f(){ return(1+1) } ; f()', [None, 2]),
    ('func arg no body return', 'def f(x){ return(x*10) } ; f(2)', [None, 20]),
    ('func no arg return', r'def f(){ let x = 10.5 \n return(x*2) } \n f()', [None, 21]),
    ('func no body return', r'def f(a,b){ return((b/-3)+a*2) } \n f(10,6)', [None, 18]),
    ('1 line func arg body return', r'def f(a,b){ return((b/-3)+a*2) } ; f(10,6)', [None, 18]),
    ('1 line func no-body return', r'def f(a,b){ return((b/-3)+a*2) } \n f(10,6)', [None, 18])
]

function_expressions = [
    ('2 func nested expr', "def f(a){ return(a+1) } ; def g(a){ return(a*10) } ; 1.5 + f(g(1)-6)",
     [None, None, 6.5]),
    ('2 func bool comp expr (1)', "def f(a){return(a+1)} ; def g(a){return(a*10)} ; f(4)+1 == 7 or g(1) < 9",
     [None, None, False]),
    ('2 func bool comp expr (2)', "def f(a){return(a+1)} ; def g(a){return(a*10)} ; f(4)+1 == 7 or g(1)>9",
     [None, None, True]),
    ('2 func nested arg expr', r'def f(a,b){ let c = (a+1)/(b - 1) \n return(c) } ; def g(x){return(x+1)} ; '
                               r' f( g(1), 7 ) + 2', [None, None, 2.5]),
]

basic_if_statements = [
    ('basic if, True', "let x = -1 ; if( x > 0 ) then x = 0", -1),
    ('basic if, False', "let x = -1 ; if( x < 0 ) then x = 0", 0),
    ('basic if then, True', "let x = -1 ; if( x > 0 ) then x = 0", -1),
    ('basic if then, False', "let x = -1 ; if( x < 0 ) then x = 0", 0),
    #('basic if block, True', "f(x)=>{let c=x+1; return(c)} ; if(0 < 5){let y = f(0)*2 ; y=y+1 }",  [None, ])
    # ('basc if else stmt let x = 0; if( x < 0 ) then x = -10; else x = 10; ", )
]


class TestInterpreter(TestCase):
    def test_arithmetic_two_args(self):
        for m, p1 in two_arg_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(eval(p1), program.output)

    def test_compound_negatives(self):
        for m, p1, ans in compound_negatives:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_harder_arithmetic(self):
        for m, p1 in harder_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '='*30)
                self.assertEqual(eval(p1), program.output)

    def test_implicit_multiplication(self):
        for m, p1, ans in implicit_multiply:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '='*30)
                self.assertEqual(ans, program.output)

    def test_boolean_simple_and_or_not(self):
        for m, p1, ans in simple_and_or_not:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_bool_eq_not_eq(self):
        for m, p1, ans in equal_not_equal:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_bool_simple_comparision(self):
        for m, p1, ans in comparison:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_simple_variable_assignment(self):
        for m, p1, var, ans in simple_var_assign:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.namespace[var]}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.namespace[var])

    def test_new_line_expr(self):
        for m, p1, ans in new_line_expr:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_new_line_var(self):
        for m, p1, var, ans in new_line_var:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output[1]}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output[1])

    def test_multi_line_vars(self):
        for m, p1, var, ans in multi_line_vars:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.namespace[var]}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.namespace[var])

    def test_basic_functions(self):
        for m, p1, ans in basic_functions:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_function_expressions(self):
        for m, p1, ans in function_expressions:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)

    def test_basic_if(self):
        for m, p1, ans in basic_if_statements:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)