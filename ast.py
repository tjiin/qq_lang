import operator as op

unary_ops = {
    '-': op.neg
}
binary_ops = {
    # math
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
    '//': op.floordiv,
    '%': op.mod,
    '**': op.pow,
    # comparison
    '<': op.lt,
    '>': op.gt,
    '<=': op.le,
    '>=': op.ge,
    '==': op.eq,
    '!=': op.ne,
    # bitwise
    '|': op.or_,
    '^': op.xor,
    '&': op.and_,
    '<<': op.lshift,
    '>>': op.rshift,
}
boolean_ops = {
    'not': lambda x: not x,
    'and': lambda x, y: x and y,
    'or': lambda x, y: x or y,
}


class Node(object):
    pass


def print_all_namespaces():
    for name, obj in NameSpace.all_namespaces.items():
        print('\t' * 2 + f'{name}')
        for k, v in obj.space.items():
            if type(v) is Variable:
                print('\t' * 4 + f'{k} : {v} | {v.declare_type} | {v.value_type} | {v.obj}')
            elif type(v) in (Int, Float, Bool):
                print('\t' * 4 + f'{k} : {v} | {v.value}')
            elif type(v) is FunctionDef:
                print('\t' * 4 + f'{k} : {v} | {v.params} | {v.body}')
            else:
                print('\t' * 4 + f'{k} : {v}')


class NameSpace:
    all_namespaces = {}

    def __init__(self, label, parent=None):
        self.label = label
        self.space = {}
        if parent is not None:
            parent[self.label] = self  # ?
            print(f'PARENT AFTER ASSIGN: {parent}')
        NameSpace.all_namespaces[self.label] = self

    def __contains__(self, item):
        return item in self.space.keys()

    def __getitem__(self, item):
        if self.__contains__(item):
            return self.space[item]
        else:
            raise Exception(f'NameSpace Error: {item} is undefined in NameSpace {self.label}')

    def __setitem__(self, key, value):
        if value is None:
            raise Exception(f'NameSpace Error: Assigning {key} to None')
        elif type(value) not in (Variable, FunctionDef, JumpLocation, NameSpace):
            raise Exception(f'NameSpace Error: Assigning {key} to improper type {type(value)}')
        else:
            self.space[key] = value

    def __str__(self):
        return f"NameSpace '{self.label}' = {self.space}"

    def items(self):
        return set(self.space.items())

    def add_items(self, items):
        # items is a list of key,val tuples
        for k, v in items:
            self[k] = v

    def remove_child_namespace(self, child_namespace):
        if child_namespace in self:
            del self.space[child_namespace]
            del NameSpace.all_namespaces[child_namespace]
            print(f'AFTER DELETE: {self}')


class Block(Node):
    def __init__(self, tokens, statement):
        self.tokens = [tokens]
        self.statements = [statement]

    def add_statement(self, tokens, statement):
        self.tokens = [tokens] + self.tokens
        self.statements.insert(0, statement)

    def eval(self, space):
        print('=' * 10 + '\nBLOCK STRING')
        print(f'"{self.get_str()}"\n' + '=' * 10)
        results = []
        for i, s in enumerate(self.statements):
            # print(f'{i} : {s} : {s.tokens}')
            # print(s.get_str())
            if s is not None:
                r = s.eval(space)
                if type(s) is Return:
                    return r
                if type(s) is LabelledStmt:
                    s.set_location(space, self, i)
                results.append(r)
        return results

    def jump_eval(self, space, index):
        results = []
        for i, s, in enumerate(self.statements[index:]):
            if s is not None:
                r = s.eval(space)
                if type(s) is Return:
                    return r
                results.append(r)
        return results

    # ugly.. keep this running in eval along development to catch all strings
    def get_str(self):
        r = ''
        for i, s in enumerate(self.statements):
            s_i = s.get_str()
            r += s_i + ';' if s_i[-1] != '}' else s_i
            if i != len(self.statements) - 1:
                r += '\n'
        return r


class FunctionCall(Node):
    call_stack = ['@main']  # should this be a namespace object?

    def __init__(self, tokens, func, arg_list):
        self.tokens = tokens
        if isinstance(func, FunctionDef):
            self.name = func.name  # self calling FunctionDef object
            self.func_def = func
        else:
            self.name = func  # ID, str name (?)
            self.func_def = None
        self.parent_space = None
        self.args = arg_list if arg_list[0] is not None else None

    def eval(self, space):

        print(f'--EVALUATING {self.name}')
        print(space)

        if self.func_def is not None and self.name not in space:  # ?
            self.func_def.eval(space)  # self-calling function definition wasn't evaluated before being call

        FunctionCall.call_stack.append(self.name)

        if type(space) is not NameSpace:
            raise Exception(f'FunctionCall: Space is not type NameSpace in {self.name}')
        elif self.name not in space:
            raise Exception(f'Function {self.name} is undefined in {space}')

        self.parent_space = space
        parent_name = FunctionCall.call_stack[-2]
        if parent_name == self.name:
            # recursive call, if names are equal the FunctionDefs must be (?)
            # TODO: what about redefining a function and calling it under a different name?
            namespace_id = self.parent_space.label
        else:
            delim = '' if self.parent_space.label[0] == '@' else '@'
            namespace_id = f'{self.name}{delim}{self.parent_space.label}'

        # print(f'namespace_id : {namespace_id}')

        if namespace_id in NameSpace.all_namespaces:
            func_space = NameSpace.all_namespaces[namespace_id]
        else:
            func_space = NameSpace(namespace_id)  # parent=self.parent_space
            print(f'Created new NameSpace {func_space.label}')

        func_def = self.parent_space[self.name].eval(space)  # if FunctionDef is a variable we needs to eval

        args_expected = 0 if func_def.params is None else len(func_def.params)
        args_received = 0 if self.args is None else len(self.args)
        if args_received != args_expected:
            raise Exception(f'Function "{self.name}" expected {args_expected} args but got {args_received}')
        elif self.args is not None and func_def.params is not None:
            # eval args passed to function, assume all are 'let' for now
            arg_objects = [arg.eval(self.parent_space) for arg in self.args]
            # set params from function definition to evaluated arg objects (in new namespace)
            for arg_obj, param_name in zip(arg_objects, func_def.params):
                obj_type = get_result_type(arg_obj)
                var = Variable(name=param_name, declare_type='let', value_type=obj_type, obj=arg_obj)
                func_space[param_name] = var

            print(f'FunctionCall evaluated args = {arg_objects}')

        # add variables from FunctionDef space to FunctionCall space (closures and recursion)
        unshadowed_vars = [(k, v) for k, v in func_def.space.items() if k not in func_space]
        func_space.add_items(unshadowed_vars)

    # yes but what to do next?

        # eval function body
        # if no Return statement, use last statement/expr of block
        return_value = func_def.body.eval(func_space)
        if type(return_value) is list:
            return_value = return_value[-1]

        # print(f'{namespace_id} after call : {func_space.space}')

        FunctionCall.call_stack.pop()

        return return_value

    def get_str(self):
        if self.args:
            arg_strings = [x.get_str() if hasattr(x, 'get_str') else x for x in self.args]
            return f'{self.name}({",".join(arg_strings)})'
        else:
            return f'{self.name}()'


class FunctionDef(Node):
    def __init__(self, tokens, head, body):
        self.tokens = [tokens]
        self.head = head
        self.func_type = '=>' if '=>' in head else 'def'
        self.body = body[0] if len(body) == 1 else body[1]
        if self.func_type == '=>':
            self.name = head[0]
            self.params = head[2] if head[2][0] is not None else None  # careful re passing boolean params
        else:
            self.name = head[1]
            self.params = head[3] if head[3][0] is not None else None
        self.space = None

    def eval(self, space):
        # TODO: handle redefining functions..
        self.space = space
        self.space[self.name] = self
        return self  # if we want to return a function def

    def get_str(self):
        param_str = f'({",".join(self.params)})' if self.params else '()'
        body_str = '{' + str(self.body.get_str()) + '}'  # this isn't always true.. "canonical" form
        if self.func_type == '=>':
            return f'{self.name}{param_str} => {body_str}'
        else:
            return f'def {self.name}{param_str} {body_str}'


def conditional_block_eval(condition, block, space):
    if condition.eval(space):
        return block.eval(space)
    return False


class IfStmt(Node):
    def __init__(self, tokens, if_stmt, elif_list, else_stmt):
        self.tokens = [tokens]
        self.if_stmt = ConditionBlock(if_stmt[1], if_stmt[3])
        self.elif_list = [ConditionBlock(x[1], x[3]) for x in elif_list] if elif_list is not None else None
        self.else_stmt = else_stmt[2] if else_stmt != [None] else None

    def eval(self, space):
        if_result = self.if_stmt.eval(space)
        if if_result:
            return if_result
        if self.elif_list is not None:
            for elif_block in self.elif_list:
                elif_result = elif_block.eval(space)
                if elif_result:
                    return elif_result
        if self.else_stmt is not None:
            return self.else_stmt.eval(space)

    def get_str(self):
        r = f'if{self.if_stmt.expr.get_str()}' + '{\n  ' + f'{self.if_stmt.block.get_str()}' + '\n}'
        if self.elif_list:
            for case in self.elif_list:
                r += f'elif {case.expr.get_str()}' + '{\n  ' + f'{case.block.get_str()}' + '\n}'
        if self.else_stmt:
            r += 'else{\n' + f'{self.else_stmt.get_str()}' + '\n}'
        return r


class SwitchStatement(Node):
    def __init__(self, tokens, expr, case_list, default_case):
        self.tokens = tokens
        self.switch_expr = expr
        self.case_list = [ConditionBlock(x[1], x[3]) for x in case_list]
        self.default_case = default_case[2] if default_case != [None] else None

    def eval(self, space):
        switch_value = self.switch_expr.eval(space) if self.switch_expr is not None else None
        for case in self.case_list:
            if switch_value is None and case.expr.eval(space):
                return case.block.eval(space)
            elif switch_value == case.expr.eval(space):
                return case.block.eval(space)
        if self.default_case is not None:
            return self.default_case.eval(space)

    def get_str(self):
        r = 'switch ' + self.switch_expr.get_str() + ' {\n' if self.switch_expr else 'switch {\n'
        for case in self.case_list:
            r += '\tcase ' + f'{case.expr.get_str()}:' + '\n\t\t' + f'{case.block.get_str()}' + '\n'
        r += '\tdefault:\n\t\t' + self.default_case.get_str() + '\n}' if self.default_case else '}'
        return r


class CondExpr(Node):
    def __init__(self, tokens, bool_stmt, true_expr, false_expr):
        self.tokens = tokens
        self.bool_stmt = bool_stmt
        self.true_expr = true_expr
        self.false_expr = false_expr

    def eval(self, space):
        result = self.bool_stmt.eval(space)
        return self.true_expr.eval(space) if result else self.false_expr.eval(space)

    def get_str(self):
        return f'{self.bool_stmt.get_str()} ? {self.true_expr.get_str()} : {self.false_expr.get_str()}'


class ConditionBlock(Node):
    def __init__(self, expr, block):
        self.expr = expr
        self.block = block

    def eval(self, space):
        if self.expr.eval(space):
            return self.block.eval(space)
        return False


class GroupExpr(Node):
    def __init__(self, tokens, expr):
        self.tokens = tokens
        self.expr = expr

    def eval(self, space):
        return self.expr.eval(space)

    def get_str(self):
        return f'({self.expr.get_str()})'


class LabelledStmt(Node):
    def __init__(self, tokens, label, stmt):
        self.tokens = tokens
        self.label = label
        self.stmt = stmt
        self.location = None

    def eval(self, space):
        return self.stmt.eval(space)

    def set_location(self, space, block, index):
        location = JumpLocation(self.label, space, block, index)
        space[self.label] = location
        self.location = location

    def get_str(self):
        return f'{self.label}: {self.stmt.get_str()}'


class JumpLocation(Node):
    def __init__(self, label, space, block, index):
        self.label = label
        self.space = space
        self.block = block
        self.index = index
        space[label] = self

    def eval(self, space=None):
        print(f'JUMP to {self.block} at statement index {self.index}')
        return self.block.jump_eval(self.space, self.index)


class GotoStmt(Node):
    def __init__(self, tokens, label):
        self.tokens = tokens
        self.label = label

    def eval(self, space):
        if self.label not in space:
            raise Exception(f'goto label {self.label} undefined in {space}')
        location = space[self.label]
        if type(location) is not JumpLocation:
            raise Exception(f'Goto location is improper type {type(location)}')
        location.eval(space)

    def get_str(self):
        return f'goto {self.label}'


class Int(int):
    def __new__(cls, tokens, value):
        return int.__new__(cls, value)

    def __init__(self, tokens, value):
        int.__init__(value)
        self.tokens = tokens
        self.value = int(value)

    def eval(self, space):
        return self

    def get_str(self):
        return self.__str__()


class Float(float):
    def __new__(cls, tokens, value):
        return float.__new__(cls, value)

    def __init__(self, tokens, value):
        float.__init__(value)
        self.tokens = tokens
        self.value = float(value)

    def eval(self, space):
        return self

    def get_str(self):
        return self.__str__()


class Bool:
    def __init__(self, tokens, value):
        if value not in (True, 'True', False, 'False'):
            raise Exception(f'Creating Bool object with improper value {value}')
        self.tokens = tokens
        self.value = True if value in (True, 'True') else False

    def eval(self, space):
        return self

    def get_str(self):
        return self.value.__str__()

    def __bool__(self):
        return self.value


class Variable:
    def __init__(self, name, declare_type='unknown', value_type='unknown', tokens=None, obj=None):
        self.tokens = tokens
        self.declare_type = declare_type
        self.value_type = value_type
        self.name = name
        self.obj = obj

    def eval(self, space):
        var = space[self.name]
        if hasattr(var, 'obj'):
            return var.obj
        else:
            return var  # e.g. FunctionDef. Can probly be done better

    def update(self, obj):
        self.obj = obj
        self.value_type = get_result_type(obj)

    def get_str(self):
        return self.name


def get_result_type(result):
    t = type(result)
    type_dict = {
        Int: 'int',
        Float: 'float',
        Bool: 'bool',
    }
    if t in type_dict:
        return type_dict[t]
    elif t is Variable:
        return result.value_type
    elif t is FunctionDef:
        return FunctionDef
    else:
        raise Exception(f'Unknown type {t} in get_result_type()')


class Declare(Node):
    def __init__(self, tokens, declare_type, name, expr):
        self.tokens = tokens
        self.declare_type = declare_type  # 'let', 'const', 'int', 'float', 'etc'
        self.name = name
        self.expr = expr

    def eval(self, space):
        if self.name in space:
            raise Exception(f'Variable {self.name} already exists in {space.label}')
        result = self.expr.eval(space)  # should be ast object, e.g. Int, Float
        result_type = get_result_type(result)
        if self.declare_type == 'let':
            var = Variable(self.name, declare_type='let', value_type=result_type, obj=result)
        elif self.declare_type == 'const':
            var = Variable(self.name, declare_type='const', value_type=result_type, obj=result)
        else:
            # check if type is correct
            if self.declare_type != result_type:
                raise Exception(f'Variable {self.name} expected {self.declare_type} but got {result_type}')
            var = Variable(self.name, declare_type=self.declare_type, value_type=result_type, obj=result)
        space[self.name] = var
        return var  # for debug

    def get_str(self):
        return f'{self.declare_type} {self.name} = {self.expr.get_str()}'


class Assign(Node):
    def __init__(self, tokens, name, expr):
        self.tokens = [tokens.slice[i] for i in range(len(tokens))]
        self.name = name
        self.expr = expr

    def eval(self, space):
        var = space[self.name]
        if var.declare_type == 'const':
            raise Exception(f"Can't assign to const variable {self.name}")
        result = self.expr.eval(space)
        result_type = get_result_type(result)
        if var.declare_type != 'let' and result_type != var.value_type:
            raise Exception(f'Variable {self.name} expected {var.value_type} but got {result_type}')
        var.update(result)
        return var

    def get_str(self):
        return f'{self.name} = {self.expr.get_str()}'


class Return(Node):
    def __init__(self, tokens, expr):
        self.tokens = tokens
        self.expr = expr  # ?

    def eval(self, space):
        return self.expr.eval(space)

    def get_str(self):
        return f'return {self.expr.get_str()}'


def create_literal_object(tokens, val):
    val_type = type(val)
    if val_type is int:
        return Int(tokens, val)
    elif val_type is float:
        return Float(tokens, val)
    elif val_type is bool:
        return Bool(tokens, val)
    else:
        raise Exception(f'create_literal_object received unknown type {type(val)}')


class BinOp(Node):
    def __init__(self, tokens, left, oper, right):
        self.tokens = tokens
        self.left = left
        self.right = right
        self.oper = oper

    def eval(self, space):
        val = binary_ops[self.oper](self.left.eval(space), self.right.eval(space))
        return create_literal_object(self.tokens, val)

    def get_str(self):
        return f'{self.left.get_str()} {self.oper} {self.right.get_str()}'


class UnaryOp(Node):
    def __init__(self, tokens, oper, operand):
        self.tokens = [tokens]
        self.oper = oper
        self.operand = operand

    def eval(self, space):
        val = unary_ops[self.oper](self.operand.eval(space))
        return create_literal_object(self.tokens, val)

    def get_str(self):
        return f'{self.oper}{self.operand.get_str()}'


class BoolOp(Node):
    def __init__(self, tokens, oper, a, b=None):
        self.tokens = [tokens]
        self.oper = oper
        self.a = a
        self.b = b

    def eval(self, space):
        if self.oper == 'not':
            val = boolean_ops[self.oper](self.a.eval(space))
        else:
            val = boolean_ops[self.oper](self.a.eval(space), self.b.eval(space))
        # val should be python bool or ast Bool
        if type(val) is Bool:
            val = val.value
        return Bool(tokens=None, value=val)

    def get_str(self):
        if self.oper == 'not':
            return f'{self.oper} {self.a.get_str()}'
        else:
            return f'{self.a.get_str()} {self.oper} {self.b.get_str()}'