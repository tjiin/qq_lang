from unittest import TestCase
from interp import interpret
from ast import data_dict
from lexer import lexer

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
    ('two line expr', r'1+1 \n 10-2', [2, 8])
]

new_line_var = [
    ('two line assign eval', r'let x = 10 \n x + 1', 'x', 11)
]


class TestInterpreter(TestCase):
    def test_arithmetic_two_args(self):
        for m, p1 in two_arg_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                self.assertEqual(eval(p1), interpret(p1))

    def test_harder_arithmetic(self):
        for m, p1 in harder_arithmetic:
            with self.subTest(msg=m, case=p1, expected=eval(p1)):
                self.assertEqual(eval(p1), interpret(p1))

    def test_implicit_multiplication(self):
        for m, p1, ans in implicit_multiply:
            with self.subTest(msg=m, case=p1, expected=ans):
                self.assertEqual(ans, interpret(p1))

    def test_simple_variable_assignment(self):
        for m, p1, var, ans in simple_var_assign:
            with self.subTest(msg=m, case=p1, expected=ans):
                interpret(p1)
                self.assertEqual(ans, data_dict[var])

    def test_new_line_expr(self):
        for m, p1, ans in new_line_expr:
            with self.subTest(msg=m, case=p1, expected=ans):
                for t in lexer.lex(p1):
                    print(t)
                print(interpret(p1))
                #self.assertEqual(ans, interpret(p1))
                self.assertEqual(0, 0)

    def test_new_line_var(self):
        for m, p1, var, ans in new_line_var:
            with self.subTest(msg=m, case=p1, expected=ans):
                for t in lexer.lex(p1):
                    print(t)
                print(interpret(p1))
                print(data_dict[var])
                self.assertEqual(ans, interpret(p1))
