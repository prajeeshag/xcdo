# type: ignore
from dataclasses import dataclass
from typing import Any

from xcdo.core.cli.exceptions import InvalidFunction


@dataclass
class InputFailing:
    fn: Any
    e: InvalidFunction


def ff00(): ...
def ff01(i: int, s: str, k: float) -> None: ...
def ff02(i) -> None: ...
def ff03(*i: int) -> None: ...
def ff04(**i: int) -> None: ...
def ff05(i: int, *j) -> None: ...


failing = [
    InputFailing(
        ff00,
        InvalidFunction("Must have at least one and no more than two arguments", ff00),
    ),
    InputFailing(
        ff01,
        InvalidFunction("Must have at least one and no more than two arguments", ff01),
    ),
    InputFailing(
        ff02,
        InvalidFunction("Parameters should have valid type hints", ff02),
    ),
    InputFailing(
        ff03,
        InvalidFunction("Cannot have variadic arguments", ff03),
    ),
    InputFailing(
        ff04,
        InvalidFunction("Cannot have variadic arguments", ff04),
    ),
    InputFailing(
        ff05,
        InvalidFunction("Cannot have variadic arguments", ff05),
    ),
]


@dataclass
class InputPassing:
    fn: Any
    data_type: type
    requires_file_path: bool


def fp00(i: float) -> None: ...
def fp01(i: int, c) -> None: ...
def fp02(i: int, c: str) -> None: ...


passing = [
    InputPassing(fp00, float, False),
    InputPassing(fp01, int, True),
    InputPassing(fp02, int, True),
]
