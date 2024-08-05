from dataclasses import dataclass

from .argument import TokenParser
from .argument.tokens import ArgumentToken, OperatorToken
from .exceptions import OperatorNotFound, SyntaxError
from .operation import BaseOperation, Operation, ReadOperation, WriteOperation
from .registry import OperatorRegistry, ReaderRegistry, WriterRegistry


@dataclass
class CallTree:
    operators: OperatorRegistry
    writers: WriterRegistry
    readers: ReaderRegistry
    token_parser: TokenParser

    def parse_tokens(
        self, tokens: list[ArgumentToken], index: int = 0
    ) -> BaseOperation:
        token_list = list(tokens)
        opTkn = token_list.pop(0)
        if not isinstance(opTkn, OperatorToken):
            raise OperatorNotFound(str(opTkn), index)

        try:
            op = self.operators.get(opTkn.name)
        except KeyError:
            raise OperatorNotFound(opTkn.name, index)

        wrtr = self.writers.get(op.output_type)

        for i in range(op.input.len):
            rdr = self.readers.get(op.input.dtypes[i])
            tkn = token_list.pop(0)

        read_optn = ReadOperation(rdr, str(tkn))

        optn = Operation(op, (read_optn,), opTkn.params, opTkn.kwparams)
        tkn = token_list.pop(0)
        return WriteOperation(wrtr, optn, (str(tkn),))

    def tokenize(self, args: list[str]) -> list[ArgumentToken]:
        tokens: list[ArgumentToken] = []
        for i, arg in enumerate(args):
            try:
                tokens.append(self.token_parser.tokenize(arg))
            except SyntaxError as e:
                e.index = i
                raise e
        return tokens
