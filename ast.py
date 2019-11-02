from rply.token import BaseBox
from lexer import dprint
from pprint import *
global data_dict
global line_count


class Node(BaseBox):
    global data_dict
    global line_count
    data_dict = {}
    line_count = 0


class NEWLINE():
    global line_count
    line_count += 1


class Block(Node):
    def __init__(self, statement):
        #print(statement)
        self.statements = [statement]

    def add_statement(self, statement):
        #print('add_statement: ', statement)
        self.statements.append(statement)

    def eval(self):
        print('- Eval Block')
        results = []
        for i, s in enumerate(reversed(self.statements)):
            print(f'-- {i}, {s}, {s.eval()}')
            results.append(s.eval())
        if len(results) == 1:
            results = results[0]
        return results


class CompoundStatement(Node):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def eval(self):
        #print( self.first.eval(), self.second.eval() )
        #return f'{self.first.eval()} {self.second.eval()}'
        data_dict['output'] = [self.first.eval(), self.second.eval()]
        return [self.first.eval(), self.second.eval()]



class Line(Node):
    def __init__(self, token):
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


class Identifier(Node):
    def __init__(self,name):
        self.name = str(name)

    def eval(self):
        if self.name in data_dict:
            return data_dict[self.name]
        else:
            dprint(f'Identifier {self.name} is undefined')
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

    def eval(self):
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



