from rply.token import BaseBox
data_dict = {}


class Variable(BaseBox):
    def __init__(self,name,value=None):
        self.name = name
        self.value = value

    def eval(self):
        return self.value

    def update_value(self,new_value):
        self.value = new_value


class Assignment(BaseBox):
    def __init__(self,name,expr):
        self.name = name
        self.expr = expr
        self.var = Variable(name)
        #data_dict[name] = self.var

    def eval(self):
        val = self.expr.eval()
        self.var.value = val
        return val


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