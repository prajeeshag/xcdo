from dataclasses import dataclass

from .argument import TokenParser
from .argument.tokens import ArgumentToken, OperatorToken
from .exceptions import OperatorNotFound, SyntaxError
from .operation import WriteOperation
from .registry import OperatorRegistry, ReaderRegistry, WriterRegistry


@dataclass
class CallTree:
    operators: OperatorRegistry
    writers: WriterRegistry
    readers: ReaderRegistry
    token_parser: TokenParser

    def parse_arguments(self, args: list[str]) -> WriteOperation:
        tokens = self._tokenize(args)
        for i, token in enumerate(tokens):
            if not isinstance(token, OperatorToken):
                if i == 0:
                    raise OperatorNotFound(str(token), i)
                continue
            try:
                self.operators.get(token.name)
            except KeyError:
                raise OperatorNotFound(token.name, i)

    def _tokenize(self, args: list[str]) -> list[ArgumentToken]:
        tokens: list[ArgumentToken] = []
        for i, arg in enumerate(args):
            try:
                tokens.append(self.token_parser.tokenize(arg))
            except SyntaxError as e:
                e.index = i
                raise e
        return tokens
