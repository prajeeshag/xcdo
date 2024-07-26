from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._utils import inspect_function


class Writer:
    def __init__(self, fn: Callable[[Any, str], None]) -> None:
        self._fn = fn
        self._fname, params, _ = inspect_function(fn)
        if len(params) < 1 or len(params) > 2:
            raise InvalidFunction(
                "Must have at least one and no more than two arguments", self._fn
            )
        if params[0][0].startswith("*"):
            raise InvalidFunction("Cannot have variadic arguments", self._fn)

        if len(params) == 2 and params[1][0].startswith("*"):
            raise InvalidFunction("Cannot have variadic arguments", self._fn)

        if params[0][1] is None:
            raise InvalidFunction("Parameters should have valid type hints", self._fn)

        self._input_type = params[0][1]
        self._requires_file_path = False
        if len(params) == 2:
            self._requires_file_path = True

    @property
    def data_type(self) -> type:
        return self._input_type

    @property
    def requires_file_path(self) -> bool:
        return self._requires_file_path

    def __call__(self, *args: Any) -> None:
        self._fn(*args)
