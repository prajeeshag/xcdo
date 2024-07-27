from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._utils import inspect_function, type2str


class Converter:
    def __init__(self, fn: Callable[[Any], Any]) -> None:
        self._fn = fn
        name, args, self._output_type = inspect_function(self._fn)
        self._name = name
        self._check_non_none_output_type()
        self._check_single_input(args)
        self._check_non_variadic_input(args)
        self._check_type_hints(args)
        self._input_type = args[0][1]

    def _check_type_hints(self, args: Any):
        if args[0][1] is None:
            raise InvalidFunction("Parameters should have valid type hint", self._fn)

    def _check_non_variadic_input(self, args: Any):
        if args[0][0].startswith("*"):
            raise InvalidFunction("Cannot have variadic inputs", self._fn)

    def _check_single_input(self, args: Any):
        if len(args) != 1:
            raise InvalidFunction("Should take a single input", self._fn)

    def _check_non_none_output_type(self):
        if self._output_type is None or self.output_type is type(None):
            raise InvalidFunction("Cannot have a return type 'None'", self._fn)

    def __call__(self, input: Any) -> Any:
        output: object = self._fn(input)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Expected <{type2str(self.output_type)}> but received <{type2str(type(output))}> from function <{self._name}>"
            )
        return output

    @property
    def input_type(self) -> type:
        return self._input_type

    @property
    def output_type(self) -> type:
        return self._output_type
