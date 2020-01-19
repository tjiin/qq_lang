import ply.yacc as yacc
from lexer import tokens
from ast import *
from pprint import *

# TODO: Look at vscode (or other) syntax highlighting


def get_tokens(p):
    return [p.slice[i] for i in range(len(p))]


precedence = (
    ('left', 'DEF'),
    ('left', 'ID'),
    ('left', 'IF', 'ELSE'),
    ('left', 'ELIF'),
    ('left', 'ARROW'),
    ('left', 'EQUAL'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('left', 'WHILE'),
    ('left', 'COMMA'),
    ('left', 'LT', 'LE', 'GT', 'GE', 'NE', 'EQ'),
    ('left', 'PIPE'),
    ('left', 'CARET'),
    ('left', 'AMP'),
    # ('left', 'INC', 'DEC'),
    ('left', 'LSHIFT', 'RSHIFT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MUL', 'DIV', 'FLOORDIV', 'MOD'),
    ('right', 'UMINUS'),  # unary minus 'fictional' token
    ('right', 'POW'),
)


def p_main(p):
    """
    main : block
    """
    p[0] = p[1]


def p_block(p):
    """
    block : statement
          | statement block
    """
    if len(p) == 2:
        p[0] = Block(p, p[1])
    else:
        p[2].add_statement(p, p[1])
        p[0] = p[2]


def p_statement(p):
    """
    statement : stmt ';'
              | LABEL ':' stmt ';'
    """
    if p.slice[1].type == 'LABEL':
        p[0] = LabelledStmt(p, p[1], p[3])
    else:
        p[0] = p[1]


def p_goto(p):
    """
    stmt : GOTO LABEL
    """
    p[0] = GotoStmt(p, p[2])


def p_empty(p):
    """empty : """
    pass


def p_func_def_statement(p):
    """
    statement : func_def
    """
    p[0] = p[1]


def p_func_def(p):
    """
    func_def : func_head func_body
    """
    p[0] = FunctionDef(p, p[1], p[2])


def p_func_body(p):
    """
    func_body : '{' block '}'
              | '{' stmt '}'
              | statement
    """
    p[0] = p[1:]


def p_func_head(p):
    """
    func_head : ARROW_ID '(' param_list ')' ARROW
              | DEF FUNC_ID '(' param_list ')'
    """
    p[0] = p[1:]


def p_param_list(p):
    """
    param_list : ID
               | param_list COMMA ID
               | empty
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_func_call(p):
    """
    func_call : FUNC_ID '(' expr_list ')'
    """
    p[0] = FunctionCall(p, p[1], p[3])


def p_self_calling_function(p):
    """
    func_call : '(' func_def ')' '(' expr_list ')'
    """
    p[0] = FunctionCall(p, p[2], p[5])


def p_if_then(p):
    """
    statement : if_stmt elif_list else_stmt
    """
    p[0] = IfStmt(p, p[1], p[2], p[3])


def p_if_stmt(p):
    """
    if_stmt : IF expr '{' block '}'
    """
    p[0] = p[1:]


def p_else_stmt(p):
    """
    else_stmt : ELSE '{' block '}'
              | empty
    """
    p[0] = p[1:]


def p_elif_case(p):
    """
    elif_case : ELIF expr '{' block '}'
    """
    p[0] = [p[1:]]


def p_elif_list(p):
    """
    elif_list : elif_case
              | elif_list elif_case
              | empty
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]


def p_switch_statement(p):
    """
    statement : SWITCH switch_expr '{' case_list default_case '}'
    """
    p[0] = SwitchStatement(tokens, p[2], p[4], p[5])


def p_switch_expr(p):
    """
    switch_expr : expr
                | empty
    """
    p[0] = p[1]


def p_case_list(p):
    """
    case_list : switch_case
              | case_list switch_case
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]


def p_switch_case(p):
    """
    switch_case : CASE expr ':' block
    """
    p[0] = [p[1:]]


def p_default_case(p):
    """
    default_case : DEFAULT ':' block
                 | empty
    """
    p[0] = p[1:]


def p_ternary_op(p):
    """
    stmt : bool_expr '?' expr ':' expr
         | ID '?' expr ':' expr
    """
    # what about nested ternary?
    if p.slice[1].type == 'ID':
        p[1] = Variable(name=p[1], tokens=p.slice[1])  # ?
    p[0] = CondExpr(p, p[1], p[3], p[5])


def p_expr(p):
    """
    stmt : expr
    """
    p[0] = p[1]


def p_expr_list(p):
    """
    expr_list : expr
              | expr_list COMMA expr
              | empty
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_return(p):
    """
    stmt : RETURN expr
    """
    p[0] = Return(p, p[2])


def p_declare(p):
    """
    stmt : LET ID EQUAL expr
         | CONST ID EQUAL expr
         | INT ID EQUAL expr
         | FLOAT ID EQUAL expr
         | BOOL ID EQUAL expr
         | STRING ID EQUAL expr
    """
    p[0] = Declare(p, p[1], p[2], p[4])


def p_declare_to_function_def(p):
    """
    statement : LET ID EQUAL func_def
              | CONST ID EQUAL func_def
    """
    p[0] = Declare(p, p[1], p[2], p[4])


def p_assign(p):
    """
    expr : ID EQUAL expr
    """
    p[0] = Assign(p, p[1], p[3])


def p_bool_expr(p):
    """
    expr : bool_expr
    """
    p[0] = p[1]


def p_expr_comp(p):
    """
    bool_expr : expr LT expr
              | expr LE expr
              | expr GT expr
              | expr GE expr
              | expr NE expr
              | expr EQ expr
    """
    p[0] = BinOp(*p)


def p_expr_binop(p):
    """
    expr : expr PLUS expr
         | expr MINUS expr
         | expr MUL expr
         | expr DIV expr
         | expr FLOORDIV expr
         | expr MOD expr
         | expr POW expr
         | expr PIPE expr
         | expr CARET expr
         | expr AMP expr
         | expr LSHIFT expr
         | expr RSHIFT expr
    """
    p[0] = BinOp(*p)


def p_factor(p):
    """
    expr : constant
         | func_call
         | ID
         | '(' expr ')'
    """
    if len(p) == 2:
        if p.slice[1].type == 'ID':
            p[0] = Variable(name=p[1], tokens=p)
        else:
            p[0] = p[1]
    else:
        p[0] = GroupExpr(p, p[2])


def p_expr_uminus(p):
    """
    expr : MINUS expr %prec UMINUS
    """
    p[0] = UnaryOp(*p)


def p_bool_op(p):
    """
    bool_expr : NOT expr
              | expr AND expr
              | expr OR expr
    """
    if len(p) == 3:
        p[0] = BoolOp(p, p[1], p[2])
    else:
        p[0] = BoolOp(p, p[2], p[1], p[3])


def p_constant(p):
    """
    constant : INT_VAL
             | FLOAT_VAL
             | TRUE
             | FALSE
    """
    t = p.slice[1].type
    if t == 'INT_VAL':
        p[0] = Int(p, p[1])
    elif t == 'FLOAT_VAL':
        p[0] = Float(p, p[1])
    else:
        p[0] = Bool(p, p[1])


def p_error(p):
    # get formatted stack
    stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])
    print('Syntax error!')
    print(f'Parser State: {parser.state} | {stack_state_str} . {p}')


parser = yacc.yacc()

