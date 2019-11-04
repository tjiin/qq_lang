from rply import LexerGenerator


def dprint(*args):
    print(*args)


lg = LexerGenerator()

lg.add('LET', r'\blet\b')
lg.add('RETURN', r'\breturn\b')
lg.add('FUNCTION', r'\bfunction\b')
# lg.add('END', r"{End}")
# lg.add('START', r"{Start}")
lg.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
lg.add('COMMA', r'\,')
lg.add('INTEGER', r'(?<![\d.])[0-9]+(?![\d.])')
lg.add('FLOAT', r'\d+\.\d+')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('LBRACE', r'\{')
lg.add('RBRACE', r'\}')
lg.add('NEGATIVE', r'^-|(?<=\()-|(?<=[\+\-\*\/\^])-|(?<==\s)-')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('POW', r'\^')
lg.add('=', r'=')
# lg.add('NO_EQUALS', r'^([a-zA-Z0-9_\+\-\*\/\^\s\(\).,]+)')
lg.ignore(r'[^\S\n\t]+')
lg.add('NEWLINE', r"\\n")

lexer = lg.build()
