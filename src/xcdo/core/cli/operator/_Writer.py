from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._utils import inspect_function


class Writer:
    def __init__(
        self,
        fn: Callable[[Any, str], None],
    ) -> None:
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

    @property
    def data_type(self) -> type:
        return self._input_type

    def set_output(self, fpath: str):
        self._fpath = fpath
