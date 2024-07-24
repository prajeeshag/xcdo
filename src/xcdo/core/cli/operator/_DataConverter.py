from typing import Any, Callable

from ..exceptions import DataConverterError
from ._utils import inspect_function


class DataConverter:
    def __init__(self, fn: Callable[[Any], Any]) -> None:
        self._fn = fn
        self._input_type = type(None)
        name, args, kwargs, self._output_type = inspect_function(self._fn)
        self._name = name

        if self._output_type is None or self.output_type is type(None):
            raise DataConverterError(
                f"Invalid function definition <{name}>: DataConverter cannot not have a return type 'None'"
            )

        if kwargs:
            raise DataConverterError(
                f"Invalid function definition <{name}>: DataConverter cannot have optional inputs"
            )

        if len(args) != 1:
            raise DataConverterError(
                f"Invalid function definition <{name}>: "
                + "DataConverter should have a single input"
            )

        if args[0][0].startswith("*"):
            raise DataConverterError(
                f"Invalid function definition <{name}>: DataConverter cannot have variadic inputs"
            )
        elif args[0][1] is None:
            raise DataConverterError(
                f"Invalid function definition <{name}>: Missing type hint for parameter 'i'"
            )
        self._input_type = args[0][1]

    def __call__(self, input: Any) -> Any:
        output = self._fn(input)
        if not isinstance(output, self.output_type):
            raise DataConverterError(
                f"Expected {self.output_type} but received {type(output)} from function <{self._name}>"
            )
        return output

    @property
    def input_type(self) -> type:
        return self._input_type

    @property
    def output_type(self) -> type:
        return self._output_type
