# type: ignore
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from xcdo.core.cli.exceptions import InvalidFunction


@dataclass
class InputFailing:
    fn: Any
    e: InvalidFunction


def ff00(i): ...
def ff01(i) -> None: ...
def ff02(i, j) -> int: ...
def ff03(*i) -> int: ...
def ff04(**i) -> int: ...


failing = [
    InputFailing(ff00, InvalidFunction("Return type cannot be NoneType", ff00)),
    InputFailing(ff01, InvalidFunction("Return type cannot be NoneType", ff01)),
    InputFailing(
        ff02, InvalidFunction("Should take a single input of type <str>", ff02)
    ),
    InputFailing(
        ff03, InvalidFunction("Should take a single input of type <str>", ff03)
    ),
    InputFailing(
        ff04, InvalidFunction("Should take a single input of type <str>", ff04)
    ),
]


@dataclass
class InputPassing:
    fn: Any
    out_type: type


def fp00(i) -> int: ...


passing = [
    InputPassing(fp00, int),
]
