from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeAlias

from .operator import Generator, Operator, Reader, Writer


class BaseOperation(ABC):
    @abstractmethod
    def execute(self) -> object | None:
        raise NotImplementedError


class ChainableOperation(BaseOperation):
    pass


@dataclass
class LeafOperation(ChainableOperation):
    operator: Generator | Reader
    args: tuple[str, ...] = ()
    kwargs: tuple[tuple[str, str], ...] = ()

    def execute(self) -> object:
        if isinstance(self.operator, Generator):
            return self.operator(
                *self.operator.load_args(self.args),
                **self.operator.load_kwargs(dict(self.kwargs)),
            )
        else:
            return self.operator(self.args[0])


OperationType: TypeAlias = "Operation"


@dataclass
class Operation(ChainableOperation):
    operator: Operator
    args: tuple[str, ...] = ()
    kwargs: tuple[tuple[str, str], ...] = ()
    children: tuple[ChainableOperation, ...] = ()

    def execute(self) -> object:
        args = self.operator.load_args(self.args)
        kwargs = self.operator.load_kwargs(dict(self.kwargs))
        input = tuple(child.execute() for child in self.children)
        return self.operator(input, *args, **kwargs)


@dataclass
class RootOperation(BaseOperation):
    operator: Writer
    child: Operation
    args: tuple[str, ...] = ()

    def execute(self) -> None:
        self.operator(self.child.execute(), *self.args)
