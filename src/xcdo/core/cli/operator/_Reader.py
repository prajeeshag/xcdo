import inspect
from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._utils import inspect_function, type2str

# type casting from string is trivial, others should use DataReaders
_BASE_PARAM_DATA_TYPES = [str, int, float]

_EMPTY = inspect.Parameter.empty


class Reader:
    def __init__(
        self,
        fn: Callable[[str], object],
    ) -> None:
        self._fn = fn
        self._fname, params, output = inspect_function(fn)
        if output is None or output is type(None):
            raise (InvalidFunction("Return type cannot be NoneType", fn))
        if len(params) != 1:
            raise (InvalidFunction("Should take a single input of type <str>", fn))
        if params[0][0].startswith("*"):
            raise (InvalidFunction("Should take a single input of type <str>", fn))
        self._output_type = output

    @property
    def output_type(self):
        return self._output_type

    def __call__(self, input: str) -> Any:
        output = self._fn(input)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Promised <{type2str(self.output_type)}> but recieved <{type2str(type(output))}> from function <{self._fname}>"
            )
        return output
