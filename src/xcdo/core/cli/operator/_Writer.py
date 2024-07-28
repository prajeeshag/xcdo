from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._Operator import Operator


class Writer(Operator):
    def __init__(self, fn: Callable[[Any, str], None] | Callable[[Any], None]) -> None:
        super().__init__(fn)
        self._validate_fn()

    def _validate_fn(self):
        if self.input.len != 1 or self.input.is_variadic or self.input.is_list_or_tuple:
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
    def dtype(self) -> type:
        return self.input.dtypes[0]
