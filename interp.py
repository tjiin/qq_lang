from lexer import lexer
from parser33 import parser
from ast import *
from pprint import *
import sys, os


# interpreter will read statements from command line or a file

def interpret(code):
	return parser.parse(lexer.lex(code)).eval()


def main():

	n = len(sys.argv)
	a = sys.argv[1]
	if n > 1:
		if os.path.exists(a): 
			with open(a,'r') as f: code = f.read()
		else: 
			code = sys.argv[1]
		
		try:
			print(interpret(code))
		except Exception as e:
			print(e)
			if n == 3 and sys.argv[2] == 'a':
				for t in lexer.lex(code): 
					print(t)

			print('\n')
			print(f'data_dict = {data_dict}')	
			print(f'line_count = {line_count}')


if __name__ == '__main__':
	main()
