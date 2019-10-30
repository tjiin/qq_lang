from rply.token import BaseBox
from parser33 import dprint

global data_dict
global line_count


class Node(BaseBox):
    global data_dict
    global line_count
    data_dict = {}
    line_count = 0


class NoEquals(Node):
    def __init__(self,token):
        self.name = token.name
        self.value = token.value

    def eval(self):
        return self.name  


class Line(Node):
    def __init__(self,token):
        global data_dict
        global line_count
        self.name = token.name
        self.value = token.value
        self.line_num = line_count
        line_count += 1

    def eval(self):
        return self.name


class StructureConstant(Node):
    def __init__(self,token):
        self.name = token.name
        self.value = token.value
        self.line = Line(token)
"""        if self.name == 'START':
            line_count = 0
            data_dict = 0"""

"""    def eval(self):
        return self.name"""


class Identifier(Node):
    def __init__(self,name):
        self.name = str(name)

    def eval(self):
        if self.name in data_dict:
            dprint('name in dict')
            return data_dict[self.name]
        else:
            dprint(f'Identifier {self.name} is undefined')
            return None


class Variable(Node):
    def __init__(self,name):
        dprint('- In Var', f'{name.value}')
        self.name = name.value
        if self.name in data_dict:
            self.value = data_dict[self.name]
            dprint('in dict')
            dprint(self.value)
        else:
            self.value = None

    def eval(self):
        dprint('was here', self.value)
        #if(self.value is None)
        return self.value

    def update_value(self,new_value):
        self.value = new_value


class Assignment(Node):
    def __init__(self,name,expr):
        self.value = None
        dprint('- In Assignment')
        dprint(f'name = {name}')
        dprint(f'expr = {expr}')
        #print(f'expr.eval() = {expr.value}')
        self.name = name.value
        self.var = Variable(name)
        self.expr = expr
        result = self.expr.value
        if expr.name == 'INTEGER':
            result = int(result)
        elif expr.name == 'FLOAT':
            result = float(result)
        else:
            print('Unhandled variable case')
        data_dict[self.name] = result
        dprint('x is', type(result))
        self.var.update_value( result )

    def eval(self):
        dprint('yes2')
        val = self.expr.eval()
        self.var.update_value(val)
        data_dict[self.name] = val
        #return val


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
        #print('adding')
        #print( type(self.left.eval()), type(self.right.eval()) )
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        dprint( self.left.eval, self.right )
        dprint( type(self.left.eval()), type(self.right.eval()) )
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



