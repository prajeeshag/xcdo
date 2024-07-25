from dataclasses import dataclass
from typing import Any


@dataclass
class InputFailing:
    fn: Any
    msg: str


@dataclass
class InputDC:
    fn: Any
    input_type: type
    output_type: type


def dff00(i: int, j: int) -> int: ...
def dff01(i: int = 1) -> str: ...
def dff02(*i: int) -> int: ...
def dcf05() -> str: ...
def dcf06(i: str) -> None: ...
def dcf07(i: str): ...
def dcf08(i) -> int: ...  # type: ignore


dcfailing = [
    InputFailing(
        dff00,
        "Function <dff00>: DataConverter should have a single input",
    ),
    InputFailing(
        dff01,
        "Function <dff01>: DataConverter cannot have optional inputs",
    ),
    InputFailing(
        dff02,
        "Function <dff02>: DataConverter cannot have variadic inputs",
    ),
    InputFailing(
        dcf05,
        "Function <dcf05>: DataConverter should have a single input",
    ),
    InputFailing(
        dcf06,
        "Function <dcf06>: DataConverter cannot not have a return type 'None'",
    ),
    InputFailing(
        dcf07,
        "Function <dcf07>: DataConverter cannot not have a return type 'None'",
    ),
    InputFailing(
        dcf08,
        "Function <dcf08>: Missing type hint for parameter 'i'",
    ),
]


def dcp03(r: float) -> str:
    return 1  # type: ignore


dcpassing = [
    InputDC(dcp03, float, str),
]

dcfailingruntime = [
    InputFailing(
        dcp03,
        "Expected <class 'str'> but received <class 'int'> from function <dcp03>",
    ),
]


def dcp04(r: float) -> str:
    return str(r)


dcpassingruntime = [
    (dcp04, str),
]
