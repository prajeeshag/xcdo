from abc import ABC, abstractmethod
from typing import final

UNLIMITED_SIZE = -1


class BaseOperator[O](ABC):
    @abstractmethod
    def execute(self) -> O:
        pass


class Operator[I, O](BaseOperator[O]):
    _children: list[BaseOperator[I]] = []

    @abstractmethod
    def input_size(self) -> int:
        pass

    @abstractmethod
    def fn(self, inputs: tuple[I, ...]) -> O:
        pass

    @final
    def add_child(self, child: BaseOperator[I]):
        self._children.append(child)

    @final
    def execute(self) -> O:
        inputs = tuple(x.execute() for x in self._children)
        return self.fn(inputs)
