from abc import ABC, abstractmethod
from typing import Any, Callable

from ._utils import inspect_function


class Operator:
    def __init__(
        self,
        fn: Callable[..., Any],
        valid_arg_types=[],
        valid_input_types=[],
    ) -> None:
        self._fn = fn
        self._parse()

    def _parse(self) -> None:
        _, args, kwargs, out_type = inspect_function(self._fn)
        arg_names: list[str] = [x[0] for x in args]
        arg_types: list[Any] = [x[1] for x in args]
        kwarg_names = [x[0] for x in kwargs]
        kwarg_types = [x[1] for x in kwargs]
        kwarg_defaults = [x[2] for x in kwargs]

        try:
            index = arg_names.index("input")
            arg_names.pop(index)
            input_type = arg_types.pop(index)

            if not hasattr(input_type, "__origin__"):
                self._input_types = [input_type]
                self._num_inputs = 1
            elif input_type.__origin__ is list:
                pass
            elif input_type.__origin__ is tuple:
                pass
        except ValueError:
            self._input_types = []
            self._num_inputs = 0

    @property
    def num_inputs(self) -> int:
        return self._num_inputs

    def get_input_type(self, n: int) -> type:
        return self._input_types[n]

    def num_args(self) -> int:
        pass

    def get_arg_type(self, n: int) -> type:
        pass

    def get_arg_name(self, n: int) -> str:
        pass

    def variadic_arg_present(self) -> bool:
        pass

    def variadic_arg_type(self) -> type:
        pass

    def kwarg_keys(self) -> tuple[str, ...]:
        pass

    def get_kwarg_type(self, key: str) -> type:
        pass

    def variadic_kwarg_present(self) -> bool:
        pass

    def variadic_kwarg_type(self) -> type:
        pass

    def output_type(self) -> None:
        pass

    def execute(self, input: tuple[Any, ...]) -> Any:
        pass
