from rply.token import BaseBox
from lexer import dprint
from pprint import *


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
            raise Exception(f'NameSpace Error: {item} is Undefined in NameSpace {self.name}')

    def __setitem__(self, key, value):
        self.space[key] = value

    def __str__(self):
        return f"NameSpace '{self.name}' = {self.space}"


class Node(BaseBox):
    pass


class Block(Node):
    def __init__(self, statement):
        # print(statement)
        self.statements = [statement]

    def add_statement(self, statement):
        # print('add_statement: ', statement)
        self.statements.append(statement)

    def eval(self, space):
        print('- Block.eval():')
        results = []
        for i, s in enumerate(reversed(self.statements)):
            print(f'  line index : {i} | statement : {s} | result = {s.eval(space)}')
            results.append(s.eval(space))
        if len(results) == 1: results = results[0]
        return results


class FunctionCall(Node):
    def __init__(self, name, args=None):
        if hasattr(name, 'gettokentype'):
            name = name.value
        self.name = name
        self.args = args
        self.parent_space = None

    def eval(self, space):
        print(f'FunctionCall : name = {self.name}')
        print(f'FunctionCall : args = {self.args}')

        if type(space) != NameSpace:
            raise Exception(f"FunctionCall Error: space is not type NameSpace in {self.name}")

        self.parent_space = space
        print(self.name)

        if self.name not in self.parent_space:
            raise Exception(f"NameSpace Error: function '{self.name}' is Undefined in NameSpace '{self.parent_space}'")

        namespace_id = f'{self.name}@{self.parent_space.name}({id(self)})'
        func_space = NameSpace(namespace_id)
        func_def = self.parent_space[self.name]

        # not checking if len args is correct for now
        arg_values = [arg.eval(self.parent_space) for arg in func_def.args]

        for i, arg in enumerate(func_def.args):
            func_space[arg] = arg_values[i]  # add macro method to NameSpace maybe

        func_output = func_def.block.eval(func_space)

        print(f"Final NameSpace of function '{self.name}' ('{namespace_id}') : {func_space}")

        if func_def.return_stmt is not None:
            # variable changes from block should be be reflected in func_space
            return_value = func_def.return_stmt.eval(func_space)
            print(f"Return value of function '{self.name}' in '{self.parent_space}' : {return_value}")
            return return_value
        else:
            print(f"Line outputs of function '{self.name}' in '{self.parent_space}' : {func_output}")
            return True


# block, args and return_stmt can each be None but at least block OR return are needed
class FunctionDef(Node):
    def __init__(self, name, block, args=None, return_stmt=None):
        self.name = name
        self.block = block
        self.args = args  # should always be either None or list of string names (can be length 1)
        self.return_stmt = return_stmt
        self.space = None

    def eval(self, space):
        self.space = space
        space[self.name] = self



"""class Return(Node):
    def __init__(self):
"""


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
    def __init__(self, token):
        self.name = token.name
        self.value = token.value
        self.line = Line(token)


class Identifier(Node):
    def __init__(self, name):
        self.name = name.name
        print(f"- in Identifier init self.name = '{self.name}' token = {name}")

    def eval(self, space):
        if self.name not in space:
            raise Exception(f'NameSpace Error: Identifier {self.name} is undefined in NameSpace {space.name}')
        return space[self.name]


class Variable(Node):
    def __init__(self, name):
        if hasattr(name, 'gettokentype'):
            name = name.value
        self.name = name
        self.value = None
        # print(f"- in Variable init self.name = '{self.name}'")

    def eval(self, space):
        # print(f"- in Variable.eval() self.name = '{self.name}'")
        if self.name not in space:
            raise Exception(f"NameSpace Error: Variable '{self.name}' undefined in NameSpace '{space.name}'")
        return space[self.name]  # .eval() ?

    def update_value(self, new_value):
        self.value = new_value


class Assignment(Node):
    def __init__(self, name, expr):
        dprint('- In Assignment')
        dprint(f'-- name = {name}')
        dprint(f'-- expr = {expr}')
        self.value = None
        self.name = name.value
        self.expr = expr
        # self.var = Variable(name)
        # self.eval()

    def eval(self, space, new_variable=True):
        if new_variable:
            var = Variable(self.name)
        elif self.name not in space:
            raise Exception(f"NameSpace Error: Variable '{self.name}' in Assignment ('{self.expr}') undefined in '{space.name}'")
        else:
            var = space[self.name]

        expr = self.expr
        if not hasattr(expr, 'value'):
            result = expr.eval(space)
        else:
            result = expr.value
            if type(result) is str and expr.name == 'INTEGER':
                result = int(result)
            elif type(result) is str and expr.name == 'FLOAT':
                result = float(result)
        space[self.name] = result
        var.update_value(result)


class Float(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, space):
        return self.value

    def get_str(self):
        print(str(self.value))


class Integer(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, space):
        return self.value

    def get_str(self):
        print(str(self.value))


class BinaryOp(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self, space):
        # print(self.left, self.right.eval())
        result = self.left.eval(space) + self.right.eval(space)
        # print( f'Add({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval(space) + self.right.eval(space)


class Sub(BinaryOp):
    def eval(self, space):
        result = self.left.eval(space) - self.right.eval(space)
        # print( f'Sub({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval(space) - self.right.eval(space)


class Mul(BinaryOp):
    def eval(self, space):
        # print( self.left.eval, self.right )
        return self.left.eval(space) * self.right.eval(space)


class Div(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) / self.right.eval(space)


class Pow(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) ** self.right.eval(space)


class UnaryOp(Node):
    def __init__(self, arg, op):
        self.arg = arg
        self.op = op


class FlipSign(Node):
    def __init__(self, arg):
        self.value = arg

    def eval(self, space):
        return self.value.eval(space)*(-1)



