from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

# type: ignore


@dataclass
class Input:
    fn: Any
    input_types: list[Any] = field(default_factory=list)
    args: list[tuple[str, type]] = field(default_factory=list)
    var_arg: tuple[str, type | None] = ("", None)
    kwargs: OrderedDict[str, tuple[type, Any]] = field(default_factory=OrderedDict)
    var_kwarg: tuple[str, type | None] = ("", None)
    output_type: Any = None

    def __post_init__(self):
        self.num_args: int = len(self.args)
        self.num_inputs: int = len(self.input_types)


@dataclass
class InputFailing:
    fn: Any
    msg: str


def fp00(): ...
def fp01() -> None: ...
def fp11(*params: int) -> None: ...
def fp21(i: int) -> None: ...
def fp31(**kwds: float) -> None: ...
def fp41(i: float = 1) -> None: ...


passing = [
    Input(fp00, output_type=None),
    Input(fp01, output_type=type(None)),
    Input(fp11, output_type=type(None), var_arg=("params", int)),
    Input(fp21, output_type=type(None), args=[("i", int)]),
    Input(fp31, output_type=type(None), var_kwarg=("kwds", float)),
    Input(fp41, output_type=type(None), kwargs=OrderedDict([("i", (float, 1))])),
]


def ff00(i): ...  # type: ignore


failing = [InputFailing(ff00, "Missing type hint for argument 'i' in function 'ff00'")]


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
        "Invalid function definition <dff00>: DataConverter should have a single input",
    ),
    InputFailing(
        dff01,
        "Invalid function definition <dff01>: DataConverter cannot have optional inputs",
    ),
    InputFailing(
        dff02,
        "Invalid function definition <dff02>: DataConverter cannot have variadic inputs",
    ),
    InputFailing(
        dcf05,
        "Invalid function definition <dcf05>: DataConverter should have a single input",
    ),
    InputFailing(
        dcf06,
        "Invalid function definition <dcf06>: DataConverter cannot not have a return type 'None'",
    ),
    InputFailing(
        dcf07,
        "Invalid function definition <dcf07>: DataConverter cannot not have a return type 'None'",
    ),
    InputFailing(
        dcf08,
        "Invalid function definition <dcf08>: Missing type hint for parameter 'i'",
    ),
]


@dataclass
class InputDC:
    fn: Any
    input_type: type
    output_type: type


def dcp03(r: float) -> str:
    return 1  # type: ignore


dcpassing = [
    InputDC(dcp03, float, str),
]

dcfailingruntime = [
    InputFailing(
        dcp03,
        "Expected <str> but received <int> from function <dcp03>",
    ),
]
