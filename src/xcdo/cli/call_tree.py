from dataclasses import dataclass

from .argument import TokenParser
from .operation import WriteOperation
from .registry import OperatorRegistry, ReaderRegistry, WriterRegistry


@dataclass
class CallTree:
    operators: OperatorRegistry
    writers: WriterRegistry
    readers: ReaderRegistry
    token_parser: TokenParser

    def parse_arguments(self, args: list[str]) -> WriteOperation:
        raise NotImplementedError
