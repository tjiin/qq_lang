from rply import LexerGenerator

lg = LexerGenerator()

lg.add('LET', r'^let')
lg.add('IDENTIFIER', r'[a-zA-Z_][a-zA-Z0-9_]*')
lg.add('INTEGER', r'(?<![\d.])[0-9]+(?![\d.])')
lg.add('FLOAT', r'\d+\.\d+')
lg.add('LPAREN', r'\(')
lg.add('RPAREN', r'\)')
lg.add('NEGATIVE',r'^-|(?<=\()-|(?<=[\+\-\*\/\^])-')
lg.add('PLUS', r'\+')
lg.add('MINUS', r'-')
lg.add('MUL', r'\*')
lg.add('DIV', r'/')
lg.add('POW', r'\^')
lg.add('=', r'=')
lg.add('NEWLINE', r"\\n")
lg.add('END', r"{End}")
lg.add('START', r"{Start}")
lg.add('NO_EQUALS', r'^([a-zA-Z0-9_\+\-\*\/\^\s\(\).,]+)') # TO DO: Handle assigning boolean expressions to variables

lg.ignore(r'\s')

lexer = lg.build()


# lg.add('IMPLICIT_MUL_NUM_PAREN', r"(?<![\+\-\/\*\s()])(\(){1}(?!\()")
# lg.add('IMPLICIT_MUL_)(', r'\)\(')
