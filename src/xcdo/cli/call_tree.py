from dataclasses import dataclass

from .argument import TokenParser
from .argument.tokens import ArgumentToken, OperatorToken
from .exceptions import ArgSyntaxError, OperatorNotFound
from .operation import (
    BaseOperation,
    ChainableOperation,
    GeneratorOperation,
    Operation,
    ReadOperation,
    WriteOperation,
)
from .operator import Generator
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
            raise OperatorNotFound(str(opTkn))

        try:
            op = self.operators.get(opTkn.name)
        except KeyError:
            raise OperatorNotFound(opTkn.name)

        try:
            outputtkn = token_list.pop()
        except IndexError:
            raise ArgSyntaxError(str(opTkn), msg="Missing output")

        wrtr = self.writers.get(op.output_type)

        if isinstance(op, Generator):
            optn = GeneratorOperation(op, opTkn.params, opTkn.kwparams)
        else:
            child_optns: list[ChainableOperation] = []
            if op.input.is_variadic:
                if len(token_list) == 0:
                    raise ArgSyntaxError(str(opTkn), msg="Missing inputs")
                rdr = self.readers.get(op.input.dtypes[0])
                for tkn in token_list:
                    child_optns.append(ReadOperation(rdr, str(tkn)))
                token_list = []
            else:
                for i in range(op.input.len):
                    rdr = self.readers.get(op.input.dtypes[i])
                    try:
                        tkn = token_list.pop(0)
                        child_optns.append(ReadOperation(rdr, str(tkn)))
                    except IndexError:
                        raise ArgSyntaxError(str(opTkn), msg="Missing inputs")

            optn = Operation(op, tuple(child_optns), opTkn.params, opTkn.kwparams)

        if len(token_list) != 0:
            raise ArgSyntaxError(str(opTkn), msg="Too many inputs")
        return WriteOperation(wrtr, optn, (str(outputtkn),))

    def tokenize(self, args: list[str]) -> list[ArgumentToken]:
        tokens: list[ArgumentToken] = []
        for arg in args:
            tokens.append(self.token_parser.tokenize(arg))
        return tokens
