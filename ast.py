from rply.token import BaseBox
from pprint import *


class Node(BaseBox):
    pass


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

    def items(self):
        return [x for x in self.space.items()]

    def add_items(self, items):
        # items is a list of key,val tuples, not checking if keys are unique
        for k, v in items:
            self.space[k] = v


class Block(Node):
    def __init__(self, statement):
        self.statements = [statement]

    def add_statement(self, statement):
        self.statements.append(statement)

    def eval(self, space):
        # print(f'\n--- Block.eval() : {list(reversed(self.statements))}')
        results = []
        for i, s in enumerate(reversed(self.statements)):
            if s is not None:
                r = s.eval(space)
                # if hasattr(s, 'name'): print(f'-line {i}  |  {s.name}  |  result = {r}')
                # else: print(f'-line {i}  |  {s}  |  result = {r}')
                results.append(r)
        results = results[0] if len(results) == 1 else results
        # print(f'--- Block.eval() output = {results}\n')
        return results


class FunctionCall(Node):
    def __init__(self, name, arg_list=None):
        self.name = name.value
        self.parent_space = None
        self.args = arg_list.args if arg_list is not None else None
        # print(f'FunctionCall.init() of "{self.name}" : self.args = {arg_list.get_str() if self.args is not None else None}')

    def eval(self, space):
        # print(f"FunctionCall : name, args = '{self.name}', {self.args}")
        if type(space) != NameSpace:
            raise Exception(f"FunctionCall Error: space is not type NameSpace in {self.name}")
        elif self.name not in space:
            raise Exception(f"NameSpace Error: function '{self.name}' is undefined in '{self.parent_space}'")
        self.parent_space = space
        namespace_id = f'{self.name}{self.parent_space.name}({id(self)})'
        func_space = NameSpace(namespace_id)
        func_def = self.parent_space[self.name]
        if func_def.params is not None:
            if len(func_def.params) != len(self.args):
                raise Exception(f"FunctionCall Error: '{self.name}' expected {len(func_def.params)} arguments"
                                f" but got {len(self.args)}")
            # evaluate arguments passed to the function
            arg_values = [arg.eval(self.parent_space) for arg in self.args]
            # print(f'FunctionCall evaluated args = {arg_values}')
            # set parameters from function definition to evaluated argument values (in new namespace)
            func_space.add_items(zip(func_def.params, arg_values))

        # print(f"FunctionCall '{self.name}' space before eval : {func_space}")
        func_output = None
        if func_def.body is not None:
            func_output = func_def.body.eval(func_space)
            # print(f"FunctionCall.eval() '{self.name}' space after block eval : {func_space}")
        if func_def.return_stmt is not None:
            # print(f"Return stmt of '{self.name}' : {func_def.return_stmt}")
            return_value = func_def.return_stmt.eval(func_space)
            # print(f"Return value of '{self.name}' in '{self.parent_space}' : {return_value}")
            return return_value
        elif func_def.body is not None:  # no return but body, print line outputs for debug and return true
            # print(f"Line outputs '{self.name}' in '{self.parent_space}' : {func_output}")
            return True


# body, param_list and return_stmt can each be None but at least body OR return are needed
class FunctionDef(Node):
    def __init__(self, name, body=None, param_list=None, return_stmt=None):
        if body == return_stmt == param_list is None:
            raise ValueError('     FunctionDef needs at least body or return')
        self.name = name.value
        self.body = body
        self.params = param_list.params if param_list is not None else None
        print(f'    FunctionDef.init() self.params = {self.params}')
        self.return_stmt = return_stmt
        print(f"    FunctionDef.init() : return = {self.return_stmt}")
        self.space = None

    def eval(self, space):
        self.space = space
        space[self.name] = self


class ParamList(Node):
    def __init__(self, param):
        self.params = [param.value]
        # print(f'ParamList.init() self.params = {self.params}')

    def append_param(self, param):
        if param.value in self.params:
            raise ValueError(f'Duplicate parameter {param.value} in ParamList.append_param()')
        self.params.append(param.value)

    def eval(self, space):
        return self.params

    def __len__(self):
        return len(self.params)


class ArgList(Node):
    def __init__(self, arg):
        self.args = [arg]  # no name or value used here as they can be expr that need eval
        # print(f'ArgList.init() self.args = {self.get_str()}')

    def append_arg(self, arg):
        self.args.append(arg)

    def eval(self, space):
        # not used in FunctionCall eval
        arg_values = [a.eval(space) if not hasattr(a, 'value') else a.value for a in self.args]
        return arg_values

    def get_str(self):
        result = []
        for a in self.args:
            if hasattr(a, 'value'): result.append(a.value)
            elif hasattr(a, 'name'): result.append(a.name)
            else: result.append(a)
        return str(result)

    def __len__(self):
        return len(self.args)


class WhileLoop(Node):
    def __init__(self, bool_stmt, block):
        self.bool_stmt = bool_stmt
        self.block = block

    def eval(self, space):
        print(f"WhileLoop.eval() : bool_stmt , block = {self.bool_stmt} , {self.block}")
        i = 0
        while self.bool_stmt.eval(space):
            result = self.block.eval(space)
            print(f"WhileLoop.eval() : i = {i} | result = {result}")

        print(f"WhileLoop.eval() : exited loop, i = {i}")


class Identifier(Node):
    def __init__(self, name):
        self.name = name.name
        print(f"- in Identifier init self.name = '{self.name}' token = {name}")

    def eval(self, space):
        if self.name not in space:
            raise Exception(f"NameSpace Error: Identifier {self.name} is undefined in '{space.name}'")
        return space[self.name]


class Variable(Node):
    def __init__(self, name):
        if hasattr(name, 'gettokentype'): name = name.value
        self.name = name

    def eval(self, space):
        if self.name not in space:
            raise Exception(f"NameSpace Error: Variable '{self.name}' undefined in '{space.name}'")
        return space[self.name]  # .eval() ?


class Assignment(Node):
    def __init__(self, name, expr):
        # print(f'Assignment.init() : name = {name.value} | expr = {expr}')
        self.name = name.value
        self.expr = expr

    def eval(self, space):
        if self.name in space:
            # print(f'Assignment.eval() : Variable {self.name} already defined = {space[self.name]}')
            pass
        expr = self.expr
        if not hasattr(self.expr, 'value'):  # not a constant
            result = self.expr.eval(space)
        else:
            result = self.expr.value
            if type(result) is str and self.expr.name == 'INT': result = Int(result)
            elif type(result) is str and self.expr.name == 'FLOAT': result = float(result)
        # print(f'Assignment.eval() : "{self.name}" = {self.expr} = "{result}"')
        space[self.name] = result
        return result


# check if boolean expr? create new class
class IfStmt(Node):
    def __init__(self, condition, block, elif_list=None, else_stmt=None):
        self.condition = condition
        self.block = block
        self.elif_list = elif_list
        self.else_stmt = else_stmt
        self.space = None
        print(f"IfStmt.init() : condition = {condition}  |  block = {block} ")

    # We could define a smaller boolean statement evaluator that both If and Elif use
    # - only has condition and block
    def eval(self, space):
        result = self.condition.eval(space)
        # print(f'IfStmt.eval() : if condition -> {result}')
        if result: return self.block.eval(space)   # IF
        elif self.elif_list:  #is not None         # ELIF
            for i,condition in enumerate(self.elif_list.conditions):  # lambda or map?
                elif_cond_eval = condition.eval(space)
                # print(f'IfStmt.eval() : elif i={i} | {condition} | {condition.left} , {condition.right} -> {elif_cond_eval}')
                if elif_cond_eval:
                    # print(f'IfStmt.eval() : elif index {i} ({condition}) -> True')
                    # print(f'- IfStmt.eval() : evaluating elif block {self.elif_list.blocks[i]}')
                    elif_output = self.elif_list.blocks[i].eval(space)
                    return elif_output
        if self.else_stmt is not None:           # ELSE
            # print(f'IfStmt.eval() : No true elif, evaluating else block ({self.else_stmt})')
            else_output = self.else_stmt.eval(space)
            # print(f'IfStmt.eval() : - else block eval returned {else_output}')
            return else_output
        else: return None # Single if or if/elif with no else


class ElifCases(Node):
    def __init__(self, condition, block):
        self.conditions = [condition]
        self.blocks = [block]

    def append_case(self, condition, block):
        self.conditions.append(condition)
        self.blocks.append(block)

    def eval(self, space):
        pass

    def __len__(self):
        return len(self.conditions)


class ConditionalExpression(Node):
    def __init__(self, bool_stmt, if_true_expr, if_false_expr):
        self.bool_stmt = bool_stmt
        self.if_true_expr = if_true_expr
        self.if_false_expr = if_false_expr

    def eval(self, space):
        result = self.bool_stmt.eval(space)
        if result:
            return self.if_true_expr.eval(space)
        else:
            return self.if_false_expr.eval(space)


class Float(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, space):
        return self.value

    def get_str(self):
        print(str(self.value))


class Int(Node):
    def __init__(self, value):
        self.value = value

    def eval(self, space):
        return self.value

    def get_str(self):
        print(str(self.value))


class Not(Node):
    def __init__(self, expr):
        self.expr = expr

    def eval(self, space):
        return not(self.expr.eval(space))


class BinaryOp(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class TrueT(Node):
    def eval(self):
        return True


class FalseT(Node):
    def eval(self):
        return False


class LessThanEq(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) <= self.right.eval(space)


class LessThan(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) < self.right.eval(space)


class GreaterThan(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) > self.right.eval(space)


class GreaterThanEq(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) >= self.right.eval(space)


class NotEqual(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) != self.right.eval(space)


class EqualTo(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) == self.right.eval(space)


class And(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) and self.right.eval(space)


class Or(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) or self.right.eval(space)


class Add(BinaryOp):
    def eval(self, space):
        # print(f'Add.eval() left,right = {self.left, self.right}')
        # result = self.left.eval(space) + self.right.eval(space)
        # print( f'Add({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval(space) + self.right.eval(space)


class Sub(BinaryOp):
    def eval(self, space):
        # result = self.left.eval(space) - self.right.eval(space)
        # print( f'Sub({self.left.eval()}, {self.right.eval()}) = {result}' )
        return self.left.eval(space) - self.right.eval(space)


class Mul(BinaryOp):
    def eval(self, space):
        # print( self.left.eval(space), self.right.eval(space) )
        return self.left.eval(space) * self.right.eval(space)


class Div(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) / self.right.eval(space)


class Pow(BinaryOp):
    def eval(self, space):
        return self.left.eval(space) ** self.right.eval(space)


class FlipSign(Node):
    def __init__(self, arg):
        self.expr = arg

    def eval(self, space):
        return self.expr.eval(space) * -1


class UnaryOp(Node):
    def __init__(self, arg, oper):
        self.arg = arg
        self.oper = oper
