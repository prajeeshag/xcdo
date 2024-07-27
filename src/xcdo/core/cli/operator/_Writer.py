from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._Operator import Operator


class Writer(Operator):
    def __init__(self, fn: Callable[[Any, str], None] | Callable[[Any], None]) -> None:
        super().__init__(fn)
        if self.num_inputs != 1:
            raise InvalidFunction("Must take a single 'input'", self._fn)

        if self.num_args > 1:
            raise InvalidFunction(
                "Cannot have more than two arguments, including 'input'", self._fn
            )

        if self.num_args and self.get_arg(0).dtype is not str:
            raise InvalidFunction("The second argument must be of type <str>", self._fn)

        if self.output_type is not type(None):
            raise InvalidFunction("Should return 'None'", self._fn)

        if self.required_kwarg_keys or self.optional_kwarg_keys:
            raise InvalidFunction("Cannot have keyword arguments", self._fn)

        if self.var_arg or self.var_kwarg:
            raise InvalidFunction("Cannot have variadic arguments", self._fn)

    @property
    def requires_file_path(self) -> bool:
        return self.num_args == 1

    @property
    def input_type(self) -> type:
        return self.get_input_type(0)
