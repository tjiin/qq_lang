from lexer import lexer
from parser import parser
from pprint import *


def f(code):
    parsed = parser.parse(lexer.lex(code))
    print(parsed)
    return parsed.eval()


def gen_tokens(code):
    return lexer.lex(code)


def main():
    statements = ['-1+1','-0.1+1','-0-1.0','-1.2*(0.001)/(-4-1)','1+1000.0/2',
                  '2.45*(1-0.89)/(4-1)*((7.1))*(((-1)))',
                  '(-1)*(-1 )/( 1 - 1*(-1))', '2(5+1)', '(3-7)2',
                  '(-5)(-5)', '(1)*(2)/(3)', '2(9)',
                  'let x = 10', 'x+1', 'let temp = 98.6', 'let x = 2 * 532']

    for x in statements:
        print('-'*10)
        print(x, '=', f(x))
        pprint(data_dict)


if __name__ == '__main__':
    main()
