from abc import ABC, abstractmethod
from typing import Any, Protocol


class _OperatorFn(Protocol):
    def __call__(
        self,
        input: tuple[Any, ...] | Any,
        *args: Any,
        **kwds: Any,
    ) -> Any: ...


class Operator(ABC):
    def __init__(self, fn: _OperatorFn) -> None:
        self._fn = fn
        self._args: list[Any] = []
        self._kwargs: dict[str, Any] = {}

    @abstractmethod
    def get_num_args(self) -> int:
        pass

    @abstractmethod
    def get_arg_type(self, n: int) -> type:
        pass

    @abstractmethod
    def get_kwarg_type(self, key: str) -> type:
        pass

    @abstractmethod
    def get_input_type(self, n: int) -> None:
        pass

    @abstractmethod
    def get_num_inputs(self) -> int:
        pass

    @abstractmethod
    def get_output_type(self) -> None:
        pass

    def execute(self, input: tuple[Any, ...]) -> Any:
        return self._fn(input, *self._args, **self._kwargs)
