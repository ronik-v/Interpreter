class CodeParser:
    def __add__(self, other):
        return Concat(self, other)

    def __mul__(self, other):
        return Exp(self, other)

    def __or__(self, other):
        return Alternate(self, other)

    def __xor__(self, function):
        return LanguageProcess(self, function)


class GetValuePosToken:
    def __init__(self, token_value, token_pos):
        self.token_value = token_value
        self.token_pos = token_pos

    def __repr__(self):
        return f'TokenValuePosition({self.token_value}, {self.token_pos})'


class TokenTag(CodeParser):
    def __init__(self, token_tag):
        self.token_tag = token_tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][1] is self.token_tag:
            return GetValuePosToken(tokens[pos][0], pos + 1)
        return None


class Reserved(CodeParser):
    def __init__(self, token_value, token_tag):
        self.token_value = token_value
        self.token_tag = token_tag

    def __call__(self, tokens, pos):
        if pos < len(tokens) and tokens[pos][0] == self.token_value and tokens[pos][1] is self.token_tag:
            return GetValuePosToken(tokens[pos][0], pos + 1)
        return None


class Concat(CodeParser):
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    def __call__(self, tokens, pos):
        left_result_node = self.left_node(tokens, pos)
        if left_result_node:
            right_result_node = self.right_node(tokens, left_result_node.pos)
            if right_result_node:
                combined_value = (left_result_node.value, right_result_node.value)
                return GetValuePosToken(combined_value, right_result_node.pos)
        return None


class Exp(CodeParser):
    def __init__(self, parser, separator):
        self.parser = parser
        self.separator = separator

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)

        def process_next(parsed):
            (sepfunc, right) = parsed
            return sepfunc(result.value, right)
        next_parser = self.separator + self.parser ^ process_next

        next_result = result
        while next_result:
            next_result = next_parser(tokens, result.pos)
            if next_result:
                result = next_result
        return result


class Alternate(CodeParser):
    def __init__(self, left_node, right_node):
        self.left_node = left_node
        self.right_node = right_node

    def __call__(self, tokens, pos):
        left_result_node = self.left_node(tokens, pos)
        if left_result_node:
            return left_result_node
        right_result_node = self.right_node(tokens, pos)
        return right_result_node


class Opt(CodeParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            return result
        return GetValuePosToken(None, pos)


class Rep(CodeParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        results = []
        result = self.parser(tokens, pos)
        while result:
            results.append(result.value)
            pos = result.pos
            result = self.parser(tokens, pos)
        return GetValuePosToken(results, pos)


class LanguageProcess(CodeParser):
    def __init__(self, parser, function):
        self.parser = parser
        self.function = function

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result:
            result.value = self.function(result.value)
            return result


class Lazy(CodeParser):
    def __init__(self, parser_func):
        self.parser = None
        self.parser_func = parser_func

    def __call__(self, tokens, pos):
        if not self.parser:
            self.parser = self.parser_func()
        return self.parser(tokens, pos)


class Phrase(CodeParser):
    def __init__(self, parser):
        self.parser = parser

    def __call__(self, tokens, pos):
        result = self.parser(tokens, pos)
        if result and result.pos == len(tokens):
            return result
        return None
