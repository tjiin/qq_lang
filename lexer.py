import ply.lex as lex

literals = '(){}?;:'
token_map = (
    ('INT_VAL', r'(?<![\d.])[0-9]+(?![\d.])'),
    ('FLOAT_VAL', r'\d+\.\d+'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'\/'),
    ('MOD', r'%'),
    ('FLOORDIV', r'\/\/'),
    ('POW', r'\*\*'),
    ('PIPE', r'\|'),
    ('CARET', r'\^'),
    ('AMP', r'&'),
    # ('INC', r'\+\+'),
    # ('DEC', r'--'),
    ('TRIPCOMP', r'<=>'),
    ('LT', r'<'),
    ('LE', r'<='),
    ('GT', r'>'),
    ('GE', r'>='),
    ('EQ', r'=='),
    ('NE', r'!='),
    ('ARROW', r'=>'),
    ('LSHIFT', r'<<'),
    ('RSHIFT', r'>>'),
    ('EQUAL', r'='),
    ('COMMA', r','),
    ('LABEL', r'@[a-zA-Z]+'),
    'ARROW_ID',
    'FUNC_ID',
    'ID',

)
reserved = [
    'goto',
    'let',
    'const',
    'int',
    'float',
    'string',
    'bool',
    'return',
    'def',
    'if',
    'elif',
    'else',
    'switch',
    'case',
    'default',
    'break',
    'not',
    'and',
    'or',
    'True',
    'False',
    'while',
]
reserved_dict = {x: x.upper() for x in reserved}
tokens = [t[0] if type(t) is tuple else t for t in token_map] + list(reserved_dict.values())
globals().update({f't_{t[0]}': t[1] for t in token_map if type(t) is tuple})


def t_ARROW_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(?=\([a-zA-Z\s]*((?<=[a-zA-Z\s]),[\s]*[a-zA-Z]+[\s]*)*\)[\s]*=>)'
    return t


def t_FUNC_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*(?=\()'
    t.type = reserved_dict.get(t.value, 'FUNC_ID')  # Check for reserved words like return
    return t


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved_dict.get(t.value, 'ID')  # Check for reserved words
    return t


def t_COMMENT(t):
    r'\/\/.*|\/\*[\s\S]*\*\/'
    pass


# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print(f'Illegal character {t.value[0]}')


t_ignore = ' \t\r\f\v'
lexer = lex.lex()
