from parser33 import Compile

def main():
	program = None
	lines = []
	space = None
	last_code = None
	print('-'*10)
	while True:
		command = input("> ")
		# print(command)
		if command in ["$q","$quit"]:
			break
		elif command == "$help":
			print("inq: simple shell written in Python")
		elif command == "$lines":
			print(lines)
		elif command == "$last":
			print(last_code)
		elif len(command) > 0 and command[-1] == '?':
			if lines != []:
				lines.append(command[:-1])
				code = '\\n'.join(lines)
			else:
				code = command[:-1]
			last_code = code
			try:
				program = Compile(code, space=space, details=False)
				space = program.namespace
				print(space)
				print(program.output)
			except Exception as e:
				print('--Error--')
				print(e)
		elif command not in ['', '\n', '?']:
			lines.append(command)
		else:
			lines = []

        	#program = Compile(code)
        	#print(program.namespace)
        	#print(program.output)

main()