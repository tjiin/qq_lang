from rply import ParserGenerator
from ast import *
from lexer import *
from pprint import *
import warnings

# warnings.filterwarnings('ignore')


pg = ParserGenerator(
    # List of all token names accepted by the parser
    ['INTEGER', 'FLOAT', 'STRING', 'BOOL', 'SEMICOLON',
     'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'LSQR', 'RSQR', 'COMMA',
     'NEGATIVE', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'CARET', 'MOD',
     'LET', 'IDENTIFIER', '=', '==', '!=', 'IF', 'AND', 'OR', 'NOT', 'ELSE', 'ELIF',
     'FUNCTION', 'RETURN', '<', '>', '<=', '>=', 'TRUE', 'FALSE',
     'NEWLINE', '$end'],
    # List of precedence rules in ascending ORDER
    precedence=[
        ('left', ['LPAREN', 'RPAREN']),
        ('left', ['FUNCTION']),
        ('left', ['LET']),
        ('left', ['IDENTIFIER']),
        ('left', ['=']),
        ('left', ['COMMA']),  # fixes 1 shift/reduce, not sure if best location
        ('left', ['<=', '<', '>', '>=', '!=', '==']),
        ('left', ['NOT', 'AND', 'OR']),
        ('left', ['FLOAT', 'INTEGER']),
        ('right', ['POW']),
        ('left', ['NEWLINE']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['NEGATIVE']),
        ('left', ['MUL', 'DIV']),
    ]  # cache_id='pg_cache1'
)


@pg.production('main : block')
def program(self, p):
    return p[0]


@pg.production('block : statement')
def main_block(state, p):
    b = Block(p[0])
    return b


@pg.production('block : statement block')
def block_statement(state, p):
    print('block : statement block')
    b = p[1] if type(p[1]) is Block else Block(p[1])
    b.add_statement(p[0])
    return b


@pg.production('statement : stmt $end')
@pg.production('statement : stmt NEWLINE')
@pg.production('statement : stmt SEMICOLON')
def statement(state, p):
    return p[0]


@pg.production('stmt : function_call')
def func_call_stmt(state, p):
    return p[0]


@pg.production('stmt : function_def')
# @pg.production('stmt : function_def NEWLINE')
def func_def_stmt(state, p):
    return p[0]


@pg.production('function_call : IDENTIFIER LPAREN RPAREN')
@pg.production('function_call : IDENTIFIER LPAREN arg_list RPAREN')
def func_call(state, p):
    if len(p) == 3:
        return FunctionCall(p[0])
    else:
        return FunctionCall(p[0], p[2])


@pg.production('function_def : FUNCTION IDENTIFIER LPAREN arg_list RPAREN LBRACE return RBRACE')
def func_def_no_body(state, p):
    return FunctionDef(p[1], args=p[3], return_stmt=p[6])


#                                  0        1         2      3       4      5      6     7      8
# FunctionDef(name, block=None, args=None, return_stmt=None)
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN arg_list RPAREN LBRACE block return RBRACE')
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN arg_list RPAREN LBRACE block RBRACE')
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN arg_list RPAREN LBRACE statement RBRACE')
def func_def(state, p):
    if len(p) == 9:
        return FunctionDef(p[1], p[6], p[3], p[7])
    else:
        return FunctionDef(p[1], block=p[6], args=p[3])  # block or stmt body


#                                  0        1         2      3     4      5      6     7
# FunctionDef(name, block=None, args=None, return_stmt=None)
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE block return RBRACE')
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE block RBRACE')
@pg.production('function_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE statement RBRACE')
def func_def_no_args(state, p):
    if len(p) == 8:
        return FunctionDef(p[1], block=p[5], return_stmt=p[6])
    else:
        return FunctionDef(p[1], block=p[5])  # block or stmt body


@pg.production('function_def : FUNCTION IDENTIFIER LPAREN RPAREN LBRACE return RBRACE')
def func_def_no_arg_no_block(state, p):
    return FunctionDef(p[1], return_stmt=p[5])


# @pg.production('arg_list : IDENTIFIER')
@pg.production('arg_list : expr')
def single_arg(state, p):
    a = ArgList(p[0])
    return a


@pg.production('arg_list : expr COMMA arg_list')
# @pg.production('arg_list : IDENTIFIER COMMA arg_list')
def arg_list(state, p):
    if type(p[2]) is ArgList:
        a = p[2]
    else:
        a = ArgList(p[2])
    a.add_arg(p[0])
    return a


# @pg.production('return : RETURN LPAREN expr RPAREN')
@pg.production('return : RETURN expr')
def return_stmt(state, p):
    return p[1]


@pg.production('stmt : LET IDENTIFIER = expr')
def assign_id(state, p):
    return Assignment(p[1], p[3])


@pg.production('stmt : IDENTIFIER = expr')
def update_id(state, p):
    return Assignment(p[0], p[2])


@pg.production('stmt : expr')
def expr(state, p):
    return p[0]


@pg.production('expr : NEGATIVE expr')
def neg_expr(state, p):
    return FlipSign(p[1])


@pg.production('expr : IDENTIFIER')
def eval_id(state, p):
    return Variable(p[0])


@pg.production('expr : number')
def eval_num(state, p):
    return p[0]


@pg.production('expr : TRUE')
@pg.production('expr : FALSE')
def bool_literals(state, p):
    if p[0].gettokentype() == 'TRUE':
        return TrueT
    else:
        return FalseT


@pg.production('expr : LPAREN expr RPAREN')
def paren_expr(state, p):
    return p[1]


@pg.production('expr : expr <= expr')
@pg.production('expr : expr < expr')
@pg.production('expr : expr > expr')
@pg.production('expr : expr >= expr')
def size_comparison_ops(state, p):
    left = p[0]
    right = p[2]
    t = p[1].gettokentype()
    if t == '<=':
        return LessThanEq(left, right)
    elif t == '<':
        return LessThan(left, right)
    elif t == '>':
        return GreaterThan(left, right)
    elif t == '>=':
        return GreaterThanEq(left, right)
    else:
        raise ValueError('This should not happen!')


@pg.production('expr : expr != expr')
@pg.production('expr : expr == expr')
def equivalence_ops(state, p):
    if p[1].gettokentype() == '!=':
        return NotEqual(p[0], p[2])
    else:
        return EqualTo(p[0], p[2])


@pg.production('expr : NOT expr')
@pg.production('expr : expr AND expr')
@pg.production('expr : expr OR expr')
def boolean_ops(state, p):
    if len(p) == 2:
        return Not(p[1])
    elif p[1].gettokentype() == 'AND':
        return And(p[0], p[2])
    else:
        return Or(p[0], p[2])


@pg.production('number : FLOAT')
@pg.production('number : INTEGER')
def eval_number(state, p):
    t0 = p[0].gettokentype()
    if t0 == 'FLOAT':
        return Float(float(p[0].getstr()))
    elif t0 == 'INTEGER':
        return Integer(int(p[0].getstr()))


@pg.production('expr : expr POW expr')
@pg.production('expr : expr PLUS expr')
@pg.production('expr : expr MINUS expr')
@pg.production('expr : expr MUL expr')
@pg.production('expr : expr DIV expr')
def binary_op_expr(state, p):
    left = p[0]
    right = p[2]
    t = p[1].gettokentype()
    if t == 'PLUS':
        return Add(left, right)
    elif t == 'MINUS':
        return Sub(left, right)
    elif t == 'MUL':
        return Mul(left, right)
    elif t == 'DIV':
        return Div(left, right)
    elif t == 'POW':
        return Pow(left, right)
    else:
        raise AssertionError('This should not happen!')


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : number LPAREN expr RPAREN POW expr', precedence='POW')
def implicit_mul_num_pow(state, p):
    return Mul(p[0], Pow(p[2], p[5]))


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : number LPAREN expr RPAREN', precedence='MUL')
def implicit_mul_num_par(state, p):
    return Mul(p[0], p[2])


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : LPAREN expr RPAREN number', precedence='MUL')
def implicit_mul_par_num(state, p):
    return Mul(p[1], p[3])


# EVEN PYTHON DOESN'T EVALUATE THIS ("int or float object is not callable")
@pg.production('expr : LPAREN expr RPAREN LPAREN expr RPAREN', precedence='MUL')
def implicit_mul_par_par(state, p):
    return Mul(p[1], p[4])


@pg.error
def error_handler(state, token):
    print('\n---Parsing Error---')
    print(token.getsourcepos())
    print(token)
    print(f'state : {state}\n')
    raise ValueError("Ran into a %s where it wasn't expected" % token.gettokentype())


parser = pg.build()


def parse(code, state=NameSpace('@main')):
    result = parser.parse(lexer.lex(code), state)
    return result


class Compile:  # yes I know, this name should be in scare quotes..
    def __init__(self, code, space=None):
        self.code = code
        if space is None:
            self.namespace = NameSpace('@main')
        else:
            self.namespace = space
        self.tokens = [t for t in lexer.lex(code)]
        pprint(self.tokens)
        self.parser_output = parse(code, self.namespace)
        self.output = self.parser_output.eval(self.namespace)

    def __str__(self):
        return str(self.output)

    def print_full(self):
        tokens = self.tokens
        d = 3
        space = 15
        indent = ' ' * (space + 1)
        formatted_tokens = ('\n' + indent).join([str(tokens[i:i + d]) for i in range(0, len(tokens), d)])
        rows = [['code', f'"{self.code}"'],
                ['tokens', f'{formatted_tokens}'],
                ['parser', f'{self.parser_output}'],
                ['space', f'{self.namespace}'],
                ['output', f'"{self.output}"']]
        a = '=' * 80
        b = '-' * 80
        fmt_str = f"{{: <{space}}} {{: <{space}}}"  # "{{" to escape curly brace, equivalent to e.g. "{: <15} {: <15}"
        print('\n' + a)
        for i, row in enumerate(rows):
            print(fmt_str.format(*row))
            print(b) if i != len(rows) - 1 else print(a)
