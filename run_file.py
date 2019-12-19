from parser import Compile, print_all_namespaces
from pprint import *
import traceback

fn = 'test.qq'
with open(fn, 'r') as f:
    code = f.read()

try:
    program = Compile(code, details=True)
    space = program.namespace
    output = program.output
    print(f'GLOBAL NAMESPACE after Program : ')
    print_all_namespaces()
    if output != '':
        print(f'\nProgram Output : {output}')
except Exception as e:
    print('	---Error---')
    print(f'- Cant interpret "{code}"')
    print('\n', e, '\n')
    print(traceback.format_exc())
