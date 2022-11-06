"""
https://github.com/jayconrod/imp-interpreter/blob/master/imp_ast.py
Смотреть реалицию тут
"""

from GlobalStack import Stack


class AbstractSyntaxTree(Stack):
    pass


class ComputingTree(Stack):
    pass


class LogicalTree(Stack):
    pass


class WhileNode(AbstractSyntaxTree):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f'WhileNode({self.condition}, {self.body})'

    def expression_result(self, ad):
        condition_value = self.condition.expression_result(ad)
        while condition_value:
            self.body.expression_while(ad)
            condition_value = self.condition.expression_result(ad)


class IfNode(AbstractSyntaxTree):
    def __init__(self, condition, true_value, false_value):
        self.condition = condition
        self.true_value = true_value
        self.false_value = false_value

    def __repr__(self):
        return f'IfNode({self.condition}, {self.true_value}, {self.false_value})'

    def expression_result(self, ad):
        condition_value = self.condition.expression_result(ad)
        if condition_value:
            self.true_value.expression_result(ad)
        else:
            if self.false_value:
                self.false_value.expression_result(ad)


class OperatorNode(ComputingTree):
    def __init__(self, right, left, operator):
        self.right = right
        self.left = left
        self.operator = operator

    def __repr__(self):
        return f'OperatorNode({self.operator}, {self.left}, {self.right})'

    def expression_result(self, ad):
        global result
        _left = self.left.expression_result(ad)
        _right = self.right.expression_result(ad)
        match self.operator:
            case '+':
                result = _left + _right
            case '-':
                result = _left - _right
            case '*':
                result = _left * _right
            case '/':
                result = _left / _right
            case unknown:
                raise f'UnknownOperator - {unknown}'
        return result


class ComparisonOperatorNode(LogicalTree):
    def __init__(self, right, left, operator):
        self.right = right
        self.left = left
        self.operator = operator

    def __repr__(self):
        return f'ComparisonOperatorNode({self.operator}, {self.left}, {self.right})'

    def expression_result(self, ad):
        global result
        _left = self.left.expression_result(ad)
        _right = self.right.expression_result(ad)
        match self.operator:
            case '>':
                result = _left > _right
            case '<':
                result = _left < _right
            case '>=':
                result = _left >= _right
            case '<=':
                result = _left <= _right
            case '==':
                result = _left == _right
            case '!=':
                result = _left != _right
            case unknown:
                raise f'UnknownOperator - {unknown}'
        return result


class AndNode(LogicalTree):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'AndNode({self.left}, {self.right})'

    def expression_result(self, ad):
        _left = self.left.expression_result(ad)
        _right = self.right.expression_result(ad)
        return _left and _right


class OrNode(LogicalTree):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __repr__(self):
        return f'OrNode({self.left}, {self.right})'

    def expression_result(self, ad):
        _left = self.left.expression_result(ad)
        _right = self.right.expression_result(ad)
        return _left or _right


class NotNode(LogicalTree):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'NotNode({self.value})'

    def expression_result(self, ad):
        _value = self.expression_result(ad)
        return not _value


class NumberNode(ComputingTree):
    def __init__(self, number):
        self.number = number

    def __repr__(self):
        return f'NumberNode({self.number})'

    def expression_result(self, ad):
        return self.number


class VariableNode(ComputingTree):
    def __init__(self, variable):
        self.variable = variable

    def expression_result(self, ad):
        if self.variable in ad:
            return ad[self.variable]
        return 0


class AssignStatement(AbstractSyntaxTree):
    def __init__(self, name, aexp):
        self.name = name
        self.aexp = aexp

    def __repr__(self):
        return f'AssignStatement({self.name}, {self.aexp})'

    def eval(self, env):
        value = self.aexp.eval(env)
        env[self.name] = value


class CompoundStatement(AbstractSyntaxTree):
    def __init__(self, first, second):
        self.first = first
        self.second = second

    def __repr__(self):
        return f'CompoundStatement({self.first}, {self.second})'

    def eval(self, env):
        self.first.eval(env)
        self.second.eval(env)


class UnaryOperatorNode(AbstractSyntaxTree):
    def __init__(self, operator, expr):
        self.operator = operator
        self.expr = expr

