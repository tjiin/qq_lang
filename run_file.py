from parser import Compile
from pprint import *

fn = 'test.qq'
with open(fn, 'r') as f:
    code = f.read()

try:
    program = Compile(code, details=False)
    space = program.namespace
    output = program.output
    print(f'{space.name} : ', end='')
    pprint(space.space)
    if output != '':
        print(f'{output}')
except Exception as e:
    print('	---Error---')
    print(f'- Cant interpret "{code}"')
    print(e)
