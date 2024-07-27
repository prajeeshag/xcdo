from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._Converter import Converter


class Reader(Converter):
    def __init__(self, fn: Callable[[str], Any]) -> None:
        super().__init__(fn)
        if self.input_type is not str:
            raise InvalidFunction("Input should be of type <str>", self._fn)
