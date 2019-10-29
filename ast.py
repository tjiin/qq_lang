from rply.token import BaseBox

data_dict = {}


class Identifier(BaseBox):
    def __init__(self,name):
        self.name = str(name)

    def eval(self):
        return self.name


class Variable(BaseBox):
    def __init__(self,name):
        self.name = name.value
        if self.name in data_dict:
            self.value = data_dict[self.name]
        else:
            self.value = None

    def eval(self):
        return self.value

    def update_value(self,new_value):
        self.value = new_value


class Assignment(BaseBox):
    def __init__(self,name,expr):
        self.name = name.value
        self.var = Variable(name)
        self.expr = expr
        data_dict[self.name] = self.expr.eval()
        self.var.update_value( self.expr.eval() )

    def eval(self):
        val = self.expr.eval()
        self.var.update_value(val)
        data_dict[self.name] = val
        #return val


class Float(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def get_str(self):
        print(str(self.value))


class Integer(BaseBox):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

    def get_str(self):
        print(str(self.value))


class BinaryOp(BaseBox):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Add(BinaryOp):
    def eval(self):
        return self.left.eval() + self.right.eval()


class Sub(BinaryOp):
    def eval(self):
        return self.left.eval() - self.right.eval()


class Mul(BinaryOp):
    def eval(self):
        return self.left.eval() * self.right.eval()


class Div(BinaryOp):
    def eval(self):
        return self.left.eval() / self.right.eval()