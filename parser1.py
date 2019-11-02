from rply import ParserGenerator
from ast import *
from pprint import *
import warnings
#warnings.filterwarnings('ignore')

pg = ParserGenerator(
    # A list of all token names, accepted by the parser.
    ['INTEGER', 'FLOAT', 'OPEN_PARENS', 'CLOSE_PARENS',
     'PLUS', 'NEGATIVE', 'MINUS', 'MUL', 'DIV', 'LET', 'IDENTIFIER', '=', 'ASSIGNMENT',
     'NEWLINE', 'POW', 'START'],

    # A list of precedence rules with ascending precedence, to
    # disambiguate ambiguous production rules.
    precedence=[
        ('left', ['PLUS', 'MINUS']),
        ('left', ['MUL', 'DIV']),
        ('left', ['FLOAT', 'INTEGER', 'NEGATIVE']),
        ('right', ['POW']),
        ('left', ['IDENTIFIER']),
    ]
)

# not expected because of what comes before or after you
# {Start} 1 -> unexpected integer
# LET -> unexpected let

@pg.production('statement : START')
@pg.production('statement : LET IDENTIFIER = expression')
@pg.production('statement : expression')
def statement_expr(p):
    return p[0]

@pg.production('expression : number')
def expression_number(p):
    return p[0]

@pg.production('expression : IDENTIFIER')
def expression_id(p):
    return Variable(p[0])

@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS')
def expression_parens(p):
    return p[1]

@pg.production('pow_expression : OPEN_PARENS expression POW expression CLOSE_PARENS', precedence='POW')
def pow_expression(p):
    return Pow(p[1], p[3].eval())

@pg.production('statement : LET IDENTIFIER = expression')
def assign_expr(p):
    return Assignment(p[1], p[3])

@pg.production('expression : NEGATIVE NEGATIVE expression')
def double_negative(p):
    return p[2]

@pg.production('expression : NEGATIVE OPEN_PARENS expression CLOSE_PARENS')
def negative_paren_expr(p):
    return FlipSign(p[2])

@pg.production('number : FLOAT')
@pg.production('number : INTEGER')
@pg.production('number : NEGATIVE FLOAT')
@pg.production('number : NEGATIVE INTEGER')
def expression_float_or_int(p):
    if p[0].gettokentype() == 'FLOAT':
        return Float( float(p[0].getstr()) )
    elif p[0].gettokentype() == 'INTEGER':
        return Integer( int(p[0].getstr()) )
    elif p[0].gettokentype() == 'NEGATIVE' and p[1].gettokentype() == 'FLOAT':
        return Float( -1*float(p[1].getstr()) )
    elif p[0].gettokentype() == 'NEGATIVE' and p[1].gettokentype() == 'INTEGER':
        return Integer( -1*int(p[1].getstr()) )
    else:
        ValueError('This should not happen')

@pg.production('expression : expression POW expression')
@pg.production('expression : expression PLUS expression')
@pg.production('expression : expression MINUS expression')
@pg.production('expression : expression MUL expression')
@pg.production('expression : expression DIV expression')
def expression_binop(p):
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
        raise AssertionError('Oops, this should not be possible!')


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expression : number OPEN_PARENS expression CLOSE_PARENS POW expression', precedence='POW')
def implicit_mul_num_pow(p):
    return Mul( p[0], Pow( p[2], p[5] ) )

# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expression : number OPEN_PARENS expression CLOSE_PARENS', precedence='MUL')
def implicit_mul_num_parens(p):
    return Mul( p[0], p[2] )


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS number', precedence='MUL')
def implicit_mul_parens_num_(p):
    return Mul( p[1], p[3] )


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expression : OPEN_PARENS expression CLOSE_PARENS OPEN_PARENS expression CLOSE_PARENS', precedence='MUL')
def implicit_mul_parens_parens_(p):
    return Mul( p[1], p[4] )


@pg.error
def error_handler(token):
    print('\n--Parsing Error--')
    print(token.getsourcepos())
    print(token)
    print('\n')

    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())


parser = pg.build()
