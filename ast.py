from rply.token import BaseBox
from lexer import dprint
from pprint import *
global data_dict
global line_count


# dictionary of identifiers defined in current namespace
class NameSpace:
    def __init__(self, name):
        self.name = name
        self.space = {}

    def __contains__(self, item):
        return item in self.space.keys()

    def __getitem__(self, item):
        if self.__contains__(item):
            return self.space[item]
        else:
            print(f'NameSpace Error: {item} is Undefined in NameSpace {self.name}')
            return None

    def __setitem__(self, key, value):
        self.space[key] = value

    def __str__(self):
        return f"NameSpace '{self.name}' = {self.space}"





class Node(BaseBox):
    def __init__self(self):
        global data_dict
        global line_count
        data_dict = {}
        line_count = 0


class Block(Node):
    def __init__(self, statement):
        #print(statement)
        self.statements = [statement]

    def add_statement(self, statement):
        #print('add_statement: ', statement)
        self.statements.append(statement)

    def eval(self, space):
        print('- Block eval()')
        results = []
        for i, s in enumerate(reversed(self.statements)):
            print(f'-- {i}, {s}, {s.eval(space)}')
            results.append(s.eval(space))
        if len(results) == 1:
            results = results[0]
        return results


class FunctionCall(Node):
    def __init__(self, name, space, args=None):
        self.name = name
        self.args = args
        self.space = space

    def eval(self, space):
        print(f'FunctionCall : name = {self.name}')
        print(f'FunctionCall : args = {self.args.eval(space)}')


class FunctionDef(Node):
    def __init__(self, name, block, args=None, ret=None):
        self.name = name
        self.block = block
        self.args = args  # should always be either None or list of strings (can be length 1)
        self.ret = ret

    def eval(self):
        namespace_id = f'@{self.name}({id(self)})'
        space = NameSpace(namespace_id)`
        return self.block.eval(space)


class Return(Node):
    def __init__(self):




class ArgList(Node):
    def __init__(self, arg):
        self.args = [arg]

    def add_arg(self, arg):
        self.args.append(arg)

    def eval(self, caller, space):
        results = []
        for i, a in enumerate(reversed(self.args)):
            if type(caller) is FunctionCall:
                val = a.eval(space) if not hasattr(a, 'value') else a.value
            elif type(caller) is FunctionDef:
                val = a.name
            else:
                raise ValueError(f'Unknown caller type in ArgList.eval(): {type(caller)}')
            results.append(val)
        if len(results) == 1 and type(caller) is FunctionCall:
            results = results[0]
        return results


class Line(Node):
    def __init__(self, token):
        global data_dict
        global line_count
        self.name = token.name
        self.value = token.value
        self.line_num = line_count
        line_count += 1

    def eval(self, space):
        return self.name


class StructureConstant(Node):
    def __init__(self,token):
        self.name = token.name
        self.value = token.value
        self.line = Line(token)


class Identifier(Node):
    def __init__(self,name):
        self.name = str(name)

    def eval(self, space):
        if self.name in space:
            return space[self.name]
        else:
            print(f'NameSpace Error: Identifier {self.name} is undefined in NameSpace {space.name}')
            return None


class Variable(Node):
    def __init__(self, name):
        dprint('- In Var', f'{name.value}')
        self.name = name.value
        if self.name in data_dict:
            self.value = data_dict[self.name]
            dprint(self.value)
        else:
            self.value = None

    def eval(self, space):
        return self.value

    def update_value(self, new_value):
        self.value = new_value


class Assignment(Node):
    def __init__(self, name, expr):
        self.value = None
        dprint('- In Assignment')
        dprint(f'-- name = {name}')
        dprint(f'-- expr = {expr}')
        self.name = name.value
        self.var = Variable(name)
        self.expr = expr
        self.eval()

    def eval(self):
        expr = self.expr
        if not hasattr(expr, 'value'):
            result = expr.eval()
        else:
            result = expr.value
            if type(result) is str and expr.name == 'INTEGER':
                result = int(result)
            elif type(result) is str and expr.name == 'FLOAT':
                result = float(result)
        data_dict[self.name] = result
        self.var.update_value(result)
        #return result


class Float(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def get_str(self):
        print(str(self.value))


class Integer(Node):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def get_str(self):
        print(str(self.value))


class BinaryOp(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        #print(self.left, self.right.eval())
        result = self.left.eval() + self.right.eval()
        #print( f'Add({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        result = self.left.eval() - self.right.eval()
        #print( f'Sub({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        #dprint( self.left.eval, self.right )
        #dprint( type(self.left.eval()), type(self.right.eval()) )
        return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()


class Pow(BinaryOp):
    def eval(self):
        return pow( self.left.eval(), self.right.eval() ) 


class UnaryOp(Node):
    def __init__(self, arg, op):
        self.arg = arg
        self.op = op


class FlipSign(Node):
    def __init__(self,arg):
        self.value = arg

    def eval(self):
       return self.value.eval()*(-1)



