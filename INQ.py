#!/usr/bin/python3.7
import os
from pprint import *


def main():
	print('_'*16)
	print('='*3 + ' [ inqq ] ' + '='*3)
	print('‾'*16)
	print('...Importing language modules...')

	from parser33 import Compile

	print('-'*20)
	space = last_code = None
	lines = history = []
	while True:
		command = input("> ")
		if command in ('$q','$quit'):
			print('Bye.')
			break
		elif command in ('$r', '$restart'):
			os.execv(__file__, [' '])
		elif command in ('$h', '$help'):
			print('inqq also needs help!..')
		elif command == '$lines':
			print(lines)
		elif command == '$$':
			if len(history) > 0:
				print(history[-1])
		elif command == '$history':
			print(history)
		elif command in ('$cl', '$clear'):
			lines = []
		elif command in ('$l', '$last'):
			print(last_code)
		elif len(command) > 0 and command[-1] == '?':
			# print(f'"{command}"')
			if lines and command[:-1] not in ('', ' '):
				lines.append(command[:-1])
				print(f"	Pushed '{command[:-1]}'")
				code = ' '.join(lines)
			elif lines:
				if len(lines) == 1:
					code = lines[0]
				else:
					code = ' '.join(lines)
			else:
				code = command[:-1]
			last_code = code
			# print(f'lines : {lines}')
			try:
				program = Compile(code, space=space, details=False)
				space = program.namespace
				output = program.output
				# print(f"- Ran '{code}'")
				print(f'	{space.name} : ', end='')
				pprint(space.space)
				if output:
					print(f'	{output}')
			except Exception as e:
				print('		---Error---')
				print(f"	- Can't interpret '{code}'")
				print(e)
				code = None
			# print('lines reset\n')
			lines = []
		elif command not in ['', '\n', '?']:
			print(f"	Pushed '{command}'")
			lines.append(command)
		else:
			if lines and False:
				lines = []
				print('lines reset\n')

		if command not in ('', '?'):
			history.append(command.rsplit('?')[0])


main()