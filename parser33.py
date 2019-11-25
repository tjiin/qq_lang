from rply import ParserGenerator
from ast import *
from lexer import *
from pprint import *
import warnings
# warnings.filterwarnings('ignore')


pg = ParserGenerator(
    # List of all token names accepted by the parser
    # 'STRING', 'BOOL', 'LSQR', 'RSQR', 'CARET', 'MOD',
    ['INT', 'FLOAT', ';', '(', ')', '{', '}',  ',',  'IF', 'THEN', 'ELSE', 'ELIF', ':', '?',
     'NEG', 'PLUS', 'MINUS', 'MUL', 'DIV', 'POW', 'LET', 'ID', '=', '==', '!=', 'WHILE',
     'AND', 'OR', 'NOT', 'DEF', 'RETURN', '<', '>', '<=', '>=', 'TRUE', 'FALSE', '=>',
     'NEWLINE', '$end'],
    # List of precedence rules in ascending ORDER
    precedence=[
        ('left', ['DEF']),
        ('left', ['ID']),
        ('left', ['IF', 'ELSE']),
        ('left', ['ELIF']),
        ('left', ['=>']),
        ('left', ['=']),
        ('left', ['OR']),
        ('left', ['AND']),
        ('left', ['NOT']),
        ('left', ['WHILE']),
        ('left', [',']),
        ('left', ['<', '<=', '>', '>=', '!=', '==']),
        ('left', ['FLOAT', 'INT']),
        ('left', ['PLUS', 'MINUS']),
        ('left', ['NEG']),
        ('left', ['MUL', 'DIV']),
        ('right', ['POW']),
    ]  # cache_IDENTIFIER='pg_cache1'
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
    b = p[1] if type(p[1]) is Block else Block(p[1])
    b.add_statement(p[0])
    return b


@pg.production('statement : stmt $end')
@pg.production('statement : stmt NEWLINE')
@pg.production('statement : stmt ;')
def statement(state, p):
    return p[0]


# FunctionDef - arrow notation - no params
# - implicit return
@pg.production('stmt : ID ( ) => { block return }') 
@pg.production('stmt : ID ( ) => block')
@pg.production('stmt : ID ( ) => { block }')
def arrow_def_no_params(state, p):
    if len(p) == 5:
        return FunctionDef(p[0], body=None, param_list=None, return_stmt=p[4])
    elif len(p) == 6:
        return FunctionDef(p[0], body=p[5], param_list=None, return_stmt=None)
    else:
        return FunctionDef(p[0], body=p[5], param_list=None, return_stmt=p[6])


# FunctionDef - arrow notation
@pg.production('stmt : ID ( param_list ) => { block return }')
@pg.production('stmt : ID ( param_list ) => stmt')
@pg.production('stmt : ID ( param_list ) => { block }')
def arrow_def_params(state, p):
    if len(p) == 6:
        print('arrow no body param return')
        return FunctionDef(p[0], body=None, param_list=p[2], return_stmt=p[5])
    elif len(p) == 7:
        return FunctionDef(p[0], body=p[6], param_list=p[2], return_stmt=None)
    else:
        return FunctionDef(p[0], body=p[6], param_list=p[2], return_stmt=p[7])
    
# FunctionDef - arrow notation, params but no block
@pg.production('stmt : ID ( param_list ) => { return }')
def arrow_def_params_no_body_return(state, p):
    return FunctionDef(p[0], body=None, param_list=p[2], return_stmt=p[6])

# FunctionDef - params but no block
@pg.production('stmt : DEF ID ( param_list ) { return }')
def func_def_no_body(state, p):
    return FunctionDef(p[1], body=None, param_list=p[3], return_stmt=p[6])


# FunctionDef - args     0  1       2      3 4    5     6   7      8
@pg.production('stmt : DEF ID ( param_list ) { block return }')
@pg.production('stmt : DEF ID ( param_list ) { block }')
def func_def(state, p):
    if len(p) == 9:
        return FunctionDef(p[1], p[6], p[3], p[7])
    else:
        return FunctionDef(p[1], p[6], p[3], return_stmt=None)


# FunctionDef - no args but block    1         2     3      4      5     6      7
@pg.production('stmt : DEF ID ( ) { block return }')
@pg.production('stmt : DEF ID ( ) { block }')
def func_def_no_args(state, p):
    if len(p) == 8:
        return FunctionDef(p[1], body=p[5], param_list=None, return_stmt=p[6])
    else:
        return FunctionDef(p[1], body=p[5])


# FunctionDef - no args or block
@pg.production('stmt : DEF ID ( ) { return }')
def func_def_no_arg_no_block(state, p):
    return FunctionDef(p[1], return_stmt=p[5])


# FunctionCall
@pg.production('func_call : ID ( )')
@pg.production('func_call : ID ( arg_list )')
def func_call(state, p):
    if len(p) == 3:
        return FunctionCall(p[0])
    else:
        return FunctionCall(p[0], p[2])


@pg.production('param_list : ID')
def single_param(state, p):
    a = ParamList(p[0])
    return a


@pg.production('param_list : ID , param_list')
def param_list(state, p):
    if type(p[2]) is ParamList:
        a = p[2]
    else:
        a = ParamList(p[2])
    a.append_param(p[0])
    return a


@pg.production('arg_list : expr')
def single_arg(state, p):
    a = ArgList(p[0])
    return a


@pg.production('arg_list : expr , arg_list')
def arg_list(state, p):
    if type(p[2]) is ArgList:
        a = p[2]
    else:
        a = ArgList(p[2])
    a.append_arg(p[0])
    return a


@pg.production('return : RETURN expr')
def return_stmt(state, p):
    return p[1]


@pg.production('stmt : IF expr : stmt')
@pg.production('stmt : IF expr { block }')
#@pg.production('stmt : IF expr THEN stmt')
def if_then_stmt(state, p):
    if len(p) == 3:
        return IfStmt(p[1], p[2])
    else:
        return IfStmt(p[1],p[3])


@pg.production('stmt : IF expr { stmt } ELSE { stmt }')
@pg.production('stmt : IF expr { block } ELSE { block }')
def if_else_block(state, p):
    return IfStmt(p[1], p[3], elif_list=None, else_stmt=p[7])


@pg.production('stmt : IF expr THEN stmt ELSE stmt')
@pg.production('stmt : IF expr : stmt ELSE stmt')
def if_else_basic(state, p):
    return IfStmt(p[1], p[3], elif_list=None, else_stmt=p[5])
    #return IfStmt(p[1], p[3], elif_list=None, else_stmt=p[6])


                     # 0   1   2   3   4     5      6   7   8  9
#@pg.production('stmt : IF expr { block } elif_list', precedence='ELSE') # no else
@pg.production('stmt : IF expr { block } elif_list ELSE { block }', precedence='ELSE')
def if_elif_else_block(state, p):
    if len(p) == 6:
        print('NO ELSE')
        return IfStmt(p[1], p[3], elif_list=p[5])
    else:
        print('IF ELIF ELSE')
        return IfStmt(p[1], p[3], elif_list=p[5], else_stmt=p[8])


                     # 0   1    2    3       4       5   6
@pg.production('stmt : IF expr THEN stmt elif_list')  # no else
@pg.production('stmt : IF expr THEN stmt elif_list ELSE stmt')
def if_then_elif_else_(state, p):
    if len(p) == 5:
        print('NO ELSE')
        print(f'elif : {p[4]}')
        print(f'elif : {p[4].blocks}')
        return IfStmt(p[1], p[3], elif_list=p[4], else_stmt=None)
    else:
        print('IF ELIF ELSE')
        return IfStmt(p[1], p[3], elif_list=p[4], else_stmt=p[6])


@pg.production('elif_list : ELIF expr THEN stmt')
@pg.production('elif_list : ELIF expr { block }')
def single_elif_case(state, p):
    e = ElifCases(p[1], p[3])
    return e


"""@pg.production('elif_list : elif_case')
def single_elif_list(state, p):
    return p[0]


@pg.production('elif_list : elif_case elif_list')
def elif_list(state, p):
   if type(p[1]) is ElifCases:
       e = p[1]
   else:
       e = ElifCases(p[1], )
   e.append_case(p[0], )
   return e"""


@pg.production('condt_stmt : bool_expr ? expr : expr')
def condt_assign(state, p):
    return ConditionalExpression(p[0], p[2], p[4])


@pg.production('stmt : condt_stmt')
def condt_assign_stmt(state, p):
    return p[0]


@pg.production('stmt : LET ID = expr')
@pg.production('stmt : LET ID = condt_stmt')
def assign_id(state, p):
    return Assignment(p[1], p[3])


@pg.production('stmt : ID = expr')
# @pg.production('stmt : ID = expr = stmt ')
def update_id(state, p):
    return Assignment(p[0], p[2])


@pg.production('stmt : WHILE ( bool_expr ) { block }')
def while_loop(state, p):
    return WhileLoop(p[2], p[5])


@pg.production('stmt : expr')
def expr(state, p):
    return p[0]


@pg.production('expr : func_call')
def expr_func_call(state, p):
    return p[0]



"""#@pg.production('expr : MINUS NEG ID')
#@pg.production('expr : ID MINUS NEG')
@pg.production('expr : + + ID')
@pg.production('expr : ID + +')
def inc_dec_id(state, p):
    print( p[0].gettokentype() )
    if p[0].gettokentype() == 'PLUS' or p[1].gettokentype() == 'PLUS':
        Assignment(p[2], f'{p[0]} = {p[0]} PLUS 1')"""


@pg.production('expr : NEG expr')
def neg_expr(state, p):
    return FlipSign(p[1])


@pg.production('expr : ID')
def eval_identifier(state, p):
    return Variable(p[0])


@pg.production('expr : bool_expr')
@pg.production('expr : constant')
@pg.production('constant : number')
@pg.production('constant : bool_const')
def constant(state, p):
    return p[0]


@pg.production('expr : ( expr )')
def paren_expr(state, p):
    return p[1]


@pg.production('bool_expr : expr != expr')
@pg.production('bool_expr : expr == expr')
def equivalence_ops(state, p):
    if p[1].gettokentype() == '!=':
        return NotEqual(p[0], p[2])
    else:
        return EqualTo(p[0], p[2])


@pg.production('bool_expr : NOT expr')
@pg.production('bool_expr : expr AND expr')
@pg.production('bool_expr : expr OR expr')
def boolean_ops(state, p):
    if len(p) == 2:
        return Not(p[1])
    elif p[1].gettokentype() == 'AND':
        return And(p[0], p[2])
    else:
        return Or(p[0], p[2])


@pg.production('bool_const : TRUE')
@pg.production('bool_const : FALSE')
def bool_literals(state, p):
    return TrueT if p[0].gettokentype() == 'TRUE' else FalseT


@pg.production('bool_expr : expr >= expr')
@pg.production('bool_expr : expr <= expr')
@pg.production('bool_expr : expr < expr')
@pg.production('bool_expr : expr > expr')
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


@pg.production('number : FLOAT')
@pg.production('number : INT')
def eval_number(state, p):
    t0 = p[0].gettokentype()
    if t0 == 'FLOAT':
        return Float(float(p[0].getstr()))
    elif t0 == 'INT':
        return Int(int(p[0].getstr()))


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


# Python doesn't evaluate these ("int or float object is not callable")
@pg.production('expr : number ( expr ) POW expr', precedence='POW')
def implicit_mul_num_pow(state, p):
    return Mul(p[0], Pow(p[2], p[5]))


@pg.production('expr : number ( expr )', precedence='MUL')
def implicit_mul_num_par(state, p):
    return Mul(p[0], p[2])


@pg.production('expr : ( expr ) number', precedence='MUL')
def implicit_mul_par_num(state, p):
    return Mul(p[1], p[3])


@pg.production('expr : ( expr ) ( expr )', precedence='MUL')
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
