from abc import ABC, abstractmethod
from typing import Any, final

from .cli.operator_argument import OperatorArgument

UNLIMITED_SIZE = -1


class Operator[I, O](ABC):
    _input_operators: list["Operator[Any, I]"] = []

    @abstractmethod
    def input_size(self) -> int:
        pass

    @abstractmethod
    def fn(self, inputs: tuple[I, ...]) -> O:
        pass

    @abstractmethod
    def parse_input_operators(self, args: list[OperatorArgument]):
        pass

    @final
    def execute(self) -> O:
        inputs = tuple(x.execute() for x in self._input_operators)
        return self.fn(inputs)
