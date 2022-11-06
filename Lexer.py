from threading import Thread, ThreadError
from sys import stderr, exit
from Tokens import Token
from re import compile


class Lexer(Token):
    def __init__(self, character):
        super().__init__()
        self.character = character
        self.tokens = []
        self.pos = 0

    def get_lexer_result(self):
        while self.pos < len(self.character):
            match = None
            for token_element in self.TOKEN_ARRAY:
                pattern, tag = token_element
                regex = compile(pattern)
                match = regex.match(self.character, self.pos)
                if match:
                    text = match.group(0)
                    if tag:
                        token = (text, tag)
                        self.tokens.append(token)
                    break
            if not match:
                stderr.write(f'Wrong characters in --- {self.character[self.pos]}, line: {self.pos}')
                exit(1)
            else:
                self.pos = match.end(0)

    def __call__(self):
        try:
            Thread(target=self.get_lexer_result(), args=(1,)).run()
            return self.tokens
        except ThreadError as error:
            return error


class GetNextToken:
    def __init__(self, token_array):
        self.token_array = token_array

    def __call__(self):
        for token in self.token_array:
            yield token

    def __iter__(self):
        return self.__call__()
