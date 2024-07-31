from dataclasses import dataclass
from typing import Any, Callable

from ..exceptions import InvalidFunction
from ._Converter import Converter


@dataclass(frozen=True)
class Reader:
    pass
