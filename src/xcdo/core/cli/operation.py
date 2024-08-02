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
class ReaderOperation(ChainableOperation):
    operator: Reader
    input: str

    def execute(self) -> object:
        return self.operator(self.input)


@dataclass
class GeneratorOperation(ChainableOperation):
    operator: Generator
    args: tuple[str, ...] = ()
    kwargs: tuple[tuple[str, str], ...] = ()

    def execute(self) -> object:
        return self.operator(
            *self.operator.load_args(self.args),
            **self.operator.load_kwargs(dict(self.kwargs)),
        )


@dataclass
class Operation(ChainableOperation):
    operator: Operator
    children: tuple[ChainableOperation, *tuple[ChainableOperation, ...]]
    args: tuple[str, ...] = ()
    kwargs: tuple[tuple[str, str], ...] = ()

    def execute(self) -> object:
        args = self.operator.load_args(self.args)
        kwargs = self.operator.load_kwargs(dict(self.kwargs))
        input = tuple(child.execute() for child in self.children)
        return self.operator(input, *args, **kwargs)


@dataclass
class WriterOperation(BaseOperation):
    operator: Writer
    child: Operation
    file_paths: tuple[str, ...] = ()

    def execute(self) -> None:
        self.operator(self.child.execute(), *self.file_paths)
