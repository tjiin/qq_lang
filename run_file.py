from parser import parser
from pprint import *
from ast import *
from lexer import *
import traceback

fn = 'TEST.QQ'
with open(fn, 'r') as f:
    code = f.read()

try:
    lexer.input(code)
    for t in lexer:
        print(t)

    # result = parser.parse(code, debug=1)
    result = parser.parse(code)
    # print(result)
    space = NameSpace('@main')
    output = result.eval(space)
    print('='*20+'\nGLOBAL NAMESPACE after Program : ')
    print_all_namespaces()
    # print(output)
    print('='*10+'\nBLOCK OUTPUT')
    for x in output:
        if x is not None:  # not 'if x' !
            if type(x) is Variable:
                print(f'{x} | {x.name} | {x.declare_type} | {x.value_type} | {x.obj}', end='')
                if hasattr(x.obj, 'value'):
                    print(f' | {x.obj.value}')
                else:
                    print('\n')
            elif type(x) in (Int, Float, Bool):
                print(f'{x} | {x.value}')
            else:
                print(x)
        else:
            print(x)
except Exception as e:
    # print('	--- Error ---')
    # print(f"Can't interpret '{code}'")
    print('\n', e, '\n')
    print(traceback.format_exc())
    # print(space)


