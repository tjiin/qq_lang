from unittest import TestCase
from parser import Compile

two_arg_arithmetic = [
    ('add 2 pos', '1 + 1'), ('sub 2 pos', '8 - 4'), ('sub 2 no space', '-8-4'), ('mul 2 pos', '4 * 8',),
    ('div 2 pos', '12 / 3'), ('add 2 neg', '-10 - 9'), ('sub 2 neg', '-1 - 41'), ('mul 2 neg', '-4 * -2',),
    ('div 2 neg', '-50 / -2'), ('pow 2 pos', '2**3'), ('pow 2 neg', '-2**-3'),
]

harder_arithmetic = [
    # Remember you can't use ^ for power if you're going to use python eval to check answer
    ('add sub 3 float', '2.5 - 99.65 + 0.001'), ('mul div 3 float', '2.5 * 99.65 / 0.001'),
    ('add/sub/mul/div nest paren neg', '((-0.1)+2.5)*(-99.65/(9-0.001))+((2.7))'),
    ('add/sub/mul/div OOP', '1 + 2 - 3 * 2 / 3 - 11'),
    ('add/sub/mul/div/pow OOP (1)', '3 - 3**2 * 2 + 10 + 2**3**-1'),
    ('add/sub/mul/div/pow OOP (2)', '(1+(2-3**3))*(3-2)'),
]

negative_expressions = [
    ('sub no space', 'let x = 2; x-1', 1),
    ('neg var', 'let x = 2; -x', -2),
    ('neg expr', 'let x = 2; -(x+1);', -3),
    ('neg expr nested', 'let x = 2; -(-(x+1));', 3),
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
    ('2 line add/sub', r'1+1 ; 10-2', [2, 8]),
    ('2 line add/sub/mul/div', r' 2(-9.18/0.02) + 17 ; 1/2*(10-(-5)) ', [-901, 7.5]),
    ('3 line arithmetic', r'-3*3 ; 84/2 ; 9+8-6*5', [-9, 42, -13]),
]

new_line_var = [
    ('2 line assign eval', r'let x = 10 ; x + 1', 'x', 11),
    ('2 line neg assign eval', r'let x = -10 ; -x * -10', 'x', -100),
]

increment_decrement = [
    ('increment (x ++)', r'let x = -2; x++;', 'x', -1),
    ('increment (++ x)', r'let x = -2; ++x;', 'x', -1),
    ('decrement (x --)', r'let x = 2; x--;', 'x', 1),
    ('decrement (-- x)', r'let x = 2; --x;', 'x', 1),
]


multi_line_vars = [
    ('3 line 3 var assign/eval', r'let x = 10 ; let y = -1.5 ; let z = x * y + 3', 'z', -12.0)
]

basic_functions = [
    ('func no arg no body return', r'def f(){ return(1+1) } f()', 2),
    ('func arg no body return', 'def f(x){ return(x*10) } f(2)', 20),
    ('func no arg return', r'def f(){ let x = 10.5 ; return(x*2) } f()', 21),
    ('func no body return', r'def f(a,b){ return((b/-3)+a*2) } f(10,6)', 18),
]

function_expressions = [
    ('2 func nested expr', "def f(a){ return(a+1) } def g(a){ return(a*10) } 1.5 + f(g(1)-6)", 6.5),
    ('2 func bool comp expr (1)', "def f(a){return(a+1)} def g(a){return(a*10)} f(4)+1 == 7 or g(1) < 9", False),
    ('2 func bool comp expr (2)', "def f(a){return(a+1)} def g(a){return(a*10)} f(4)+1 == 7 or g(1)>9", True),
    ('2 func nested arg expr', r'def f(a,b){ let c = (a+1)/(b - 1) ; return(c) } def g(x){return(x+1)} '
                               r' f( g(1), 7 ) + 2', 2.5),
]

first_class_functions = [
    ('func passed as arg', 'f(g,x)=>{return(g(x))} g(y)=>y*-10; f(g,2);', -20),
    ('func returned', 'f()=>{ g(x)=>x*-3; return(g); } let h = f(); h(2);', -6),
    ('impl func return closure', 'f(x) => g(y) => x + y; let h = f(2); h(10);', 12),
    ('assign to func_def', 'let f = g(x) => x*2; f(-1);', -2),
]

basic_if_statements = [
    (' if: True', "let x=-1 ; if x > 0: x = 0", 'x', -1),
    (' if() block False', "let x = -1 ; if( x < 0 ){ x = 0; }", 'x', 0),
    (' if(): false', "let x = 25.2 ; if( x < 0 ): x = 0", 'x', 25.2),
    (' if then else true', "let x = 25.2 ; if x > 0 then x = 1 else x = -1", 'x', 1),
    (' if: else', "let x = 25.2 ; if not False: x = 0", 'x', 0),
    (' if then elif then else', "let x = 25.2 ; if x < 0 then x = 0 elif x > 30 then x = 30 else x = 1", 'x', 1)
]

three_way_cmp = [
    ('int - less', '0 <=> 1', -1),
    ('int - equal', '1 <=> 1', 0),
    ('int - greater', '1 <=> 0', 1),
]


class TestInterpreter(TestCase):
    def test_arithmetic_two_args(self):
        for m, p1 in two_arg_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(eval(p1), program.output)

    def test_harder_arithmetic(self):
        for m, p1 in harder_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(eval(p1), program.output)

    def test_negative_expressions(self):
        for m, p1, ans in negative_expressions:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output[-1])

    def test_implicit_multiplication(self):
        for m, p1, ans in implicit_multiply:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '=' * 30)
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

    def test_increment_decrement(self):
        for m, p1, var, ans in increment_decrement:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.namespace[var])

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
                self.assertEqual(ans, program.output[-1])

    def test_function_expressions(self):
        for m, p1, ans in function_expressions:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output[-1])

    def test_first_class_functions(self):
        for m, p1, ans in first_class_functions:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output[-1])

    def test_basic_if(self):
        for m, p1, var, ans in basic_if_statements:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.namespace[var])

    def test_three_way_cmp(self):
        for m, p1, ans in three_way_cmp:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} --> {program.output}' + '\n' + '=' * 30)
                self.assertEqual(ans, program.output)