from Tokens import Token
from Lexer import *
from Parser import *
from AST import *
from functools import reduce
T = Token()
num = TokenTag(T.INT) ^ (lambda value: int(value))
id = TokenTag(T.USED)
aexp_precedence_levels = [
    ['*', '/'],
    ['+', '-'],
]

bexp_precedence_levels = [
    ['and'],
    ['or'],
]


def keyword(kw):
    return Reserved(kw, T.USED)


def imp_parse(tokens):
    ast = parser()(tokens, 0)
    return ast


def parser():
    return Phrase(stmt_list())


def stmt_list():
    separator = keyword(';') ^ (lambda x: lambda l, r: CompoundStatement(l, r))
    return Exp(stmt(), separator)


def stmt():
    return assign_stmt() | \
           if_stmt() | \
           while_stmt()


def assign_stmt():
    def process(parsed):
        ((name, _), exp) = parsed
        return AssignStatement(name, exp)

    return id + keyword(':=') + aexp() ^ process


def if_stmt():
    def process(parsed):
        (((((_, condition), _), true_stmt), false_parsed), _) = parsed
        if false_parsed:
            (_, false_stmt) = false_parsed
        else:
            false_stmt = None
        return IfNode(condition, true_stmt, false_stmt)

    return keyword('if') + bexp() + \
           keyword('then') + Lazy(stmt_list) + \
           Opt(keyword('else') + Lazy(stmt_list)) + \
           keyword('end') ^ process


def while_stmt():
    def process(parsed):
        ((((_, condition), _), body), _) = parsed
        return WhileNode(condition, body)

    return keyword('while') + bexp() + \
           keyword('do') + Lazy(stmt_list) + \
           keyword('end') ^ process


def bexp():
    return precedence(bexp_term(), bexp_precedence_levels, process_logic)


def bexp_term():
    return bexp_not() | \
           bexp_relop() | \
           bexp_group()


def bexp_not():
    return keyword('not') + Lazy(bexp_term) ^ (lambda parsed: NotNode(parsed[1]))


def bexp_relop():
    relops = ['<', '<=', '>', '>=', '=', '!=']
    return aexp() + any_operator_in_list(relops) + aexp() ^ process_relop


def bexp_group():
    return keyword('(') + Lazy(bexp) + keyword(')') ^ process_group


def aexp():
    return precedence(aexp_term(), aexp_precedence_levels, process_binop)


def aexp_term():
    return aexp_value() | aexp_group()


def aexp_group():
    return keyword('(') + Lazy(aexp) + keyword(')') ^ process_group


def aexp_value():
    return (num ^ (lambda i: NumberNode(i))) | (id ^ (lambda v: VariableNode(v)))


def precedence(value_parser, precedence_levels, combine):
    def op_parser(precedence_level):
        return any_operator_in_list(precedence_level) ^ combine

    parser = value_parser * op_parser(precedence_levels[0])
    for precedence_level in precedence_levels[1:]:
        parser = parser * op_parser(precedence_level)
    return parser


def process_binop(op):
    return lambda l, r: OperatorNode(op, l, r)


def process_relop(parsed):
    ((left, op), right) = parsed
    return ComparisonOperatorNode(op, left, right)


def process_logic(op):
    if op == 'and':
        return lambda l, r: AndNode(l, r)
    elif op == 'or':
        return lambda l, r: OrNode(l, r)
    else:
        raise RuntimeError('unknown logic operator: ' + op)


def process_group(parsed):
    ((_, p), _) = parsed
    return p


def any_operator_in_list(ops):
    op_parsers = [keyword(op) for op in ops]
    parser = reduce(lambda l, r: l | r, op_parsers)
    return parser