from unittest import TestCase
from parser33 import Compile

two_arg_arithmetic = [
    ('add 2 pos', '1 + 1'), ('sub 2 pos', '8 - 4'), ('mul 2 pos', '4 * 8',), ('div 2 pos', '12 / 3'),
    ('add 2 neg', '-10 - 9'), ('sub 2 neg', '-1 - 41'), ('mul 2 neg', '-4 * -2',), ('div 2 neg', '-50 / -2'),
]

harder_arithmetic = [
    ('add sub 3 float', '2.5 - 99.65 + 0.001'), ('mul div 3 float', '2.5 * 99.65 / 0.001'),
    ('add/sub/mul/div nest paren neg', '((-0.1)+2.5)*(-99.65/(9-0.001))+((2.7))'),
    ('add/sub/mul/div OOP', '1 + 2 - 3 * 2 / 3 - 11'),
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

simple_var_assign = [
    ('var assign int', 'let x = 19', 'x', 19),
    ('var assign expr', 'let x = 19+(2*42/(-0.125))', 'x', -653),
]

new_line_expr = [
    ('2 line add/sub', r'1+1 \n 10-2', [2, 8]),
    ('2 line add/sub/mul/div', r' 2(-9.18/0.02) + 17 \n 1/2*(10-(-5)) ', [-901, 7.5]),
    ('3 line arithmetic', r'-3*3 \n 84/2 \n 9+8-6*5', [-9, 42, -13]),
]

new_line_var = [
    ('2 line assign eval', r'let x = 10 \n x + 1', 'x', 11),
]

multi_line_vars = [
    ('3 line 3 var assign/eval', r'let x = 10 \n let y = -1.5 \n let z = x * y + 3', 'z', -12.0)
]

basic_functions = [
    ('func no arg no body return', r'function f(){ return(1+1) } \n f()', [None, 2]),
    ('func no arg return', r'function f(){ let x = 10.5 \n return(x*2) } \n f()', [None, 21])
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
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '='*30)
                self.assertEqual(eval(p1), program.output)

    def test_implicit_multiplication(self):
        for m, p1, ans in implicit_multiply:
            with self.subTest(msg=m, case=p1, expected=ans):
                program = Compile(p1)
                print('=' * 30 + '\n' + f'{p1} = {program.output}' + '\n' + '='*30)
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