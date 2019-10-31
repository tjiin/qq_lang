from rply import ParserGenerator
from ast import *
from lexer import dprint
from pprint import *
import warnings
# warnings.filterwarnings('ignore')


pg = ParserGenerator(
    # List of all token names accepted by the parser
    ['INTEGER', 'FLOAT', 'STRING', 'BOOL',
     'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSQR', 'RSQR',
     'NEGATIVE', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'CARET', 'MOD',
     'LET', 'IDENTIFIER', '=', '==', '!=', 'IF', 'AND', 'OR', 'NOT', 'ELSE', 'ELIF',
     'FUNCTION', '<', '>', '<=', '>=',
     'START', 'END', 'NO_EQUALS'],
    # List of precedence rules in ascending order
    precedence=[
        ('right', ['IDENTIFIER']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV']),
        ('left', ['FLOAT', 'INTEGER']),
        ('right', ['POW']),
        ('left', ['LPAREN', 'RPAREN']),
        ('left', ['NEGATIVE']),
    ]
)

"""@pg.production('decor_const : START')
@pg.production('decor_const : END')
def decor_const(p):
    return p[0]"""


@pg.production('expr : number')
@pg.production('expr : assign')
def eval_base(p):
    return p[0]


@pg.production('expr : IDENTIFIER')
def eval_id(p):
    return Variable(p[0])


@pg.production('expr : LPAREN expr RPAREN')
def paren_expr(p):
    return p[1]


@pg.production('number : NEGATIVE FLOAT')
@pg.production('number : NEGATIVE INTEGER')
@pg.production('number : FLOAT')
@pg.production('number : INTEGER')
def eval_number(p):
    if p[0].gettokentype() == 'FLOAT':
        return Float(float(p[0].getstr()))
    elif p[0].gettokentype() == 'INTEGER':
        return Integer(int(p[0].getstr()))
    elif p[0].gettokentype() == 'NEGATIVE' and p[1].gettokentype() == 'FLOAT':
        return Float(-1 * float(p[1].getstr()))
    elif p[0].gettokentype() == 'NEGATIVE' and p[1].gettokentype() == 'INTEGER':
        return Integer(-1 * int(p[1].getstr()))
    else:
        ValueError('This should not happen!')


# @pg.production('assign : NO_EQUALS')
"""@pg.production('expr : NO_EQUALS')
def eval_no_equals(p):
	print('eval no equals')
	return p[0]
"""


@pg.production('assign : LET IDENTIFIER = expr')
def assign_id(p):
    dprint(p)
    if hasattr(p[3], 'left') and hasattr(p[3], 'left'):
        dprint(p[3].left)
        dprint(p[3].right)
    return Assignment(p[1], p[3])


"""@pg.production('update : IDENTIFIER = expr')
def update_assign(p):
    return Assignment(p[0], p[1])

@pg.production('declare : LET IDENTIFIER')
def declare_id(p):
    return Variable(p[1])"""


@pg.production('expr : NEGATIVE NEGATIVE expr')
def double_negative(p):
    return p[2]


# @pg.production('expr : FUNCTION')
# @pg.production('expr : STRING')
# @pg.production('expr : BOOL')


@pg.production('expr : NEGATIVE LPAREN expr RPAREN')
def negative_paren_expr(p):
    return FlipSign(p[2])


@pg.production('expr : expr POW expr')
@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
def binop_num_expr(p):
    left = p[0]
    right = p[2]
    if p[1].gettokentype() == 'PLUS':
        return Add(left, right)
    elif p[1].gettokentype() == 'MINUS':
        return Sub(left, right)
    elif p[1].gettokentype() == 'MUL':
        return Mul(left, right)
    elif p[1].gettokentype() == 'DIV':
        return Div(left, right)
    elif p[1].gettokentype() == 'POW':
        return Pow(left, right)
    else:
        raise AssertionError('This should not happen!')


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : number LPAREN expr RPAREN POW expr', precedence='POW')
def implicit_mul_num_pow(p):
    return Mul(p[0], Pow(p[2], p[5]))


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : number LPAREN expr RPAREN', precedence='MUL')
def implicit_mul_num_parens(p):
    return Mul(p[0], p[2])


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : LPAREN expr RPAREN number', precedence='MUL')
def implicit_mul_parens_num_(p):
    return Mul(p[1], p[3])


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : LPAREN expr RPAREN LPAREN expr RPAREN', precedence='MUL')
def implicit_mul_parens_parens_(p):
    return Mul(p[1], p[4])


@pg.error
def error_handler(token):
    print('\n--Parsing Error--')
    print(token.getsourcepos())
    print(token)
    print('\n')

    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())


parser = pg.build()

# print(parser)

# @pg.production('assert : IDENTIFIER = expr')
# @pg.production('assert : IDENTIFIER = IDENTIFIER')
