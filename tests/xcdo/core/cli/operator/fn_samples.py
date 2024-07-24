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


def ff00(i): ...  # type: ignore
def ff01(ik=1): ...  # type: ignore
def ff02(b: bool): ...  # type: ignore
def ff03(bk: list[str] = False): ...  # type: ignore


failing = [
    InputFailing(ff00, "Function <ff00>: missing type hint for parameter 'i'"),
    InputFailing(ff01, "Function <ff01>: missing type hint for parameter 'ik'"),
    InputFailing(
        ff02,
        "Function <ff02>, parameter 'b': <bool> type is not allowed "
        + "without a <str> to <bool> DataConverter",
    ),
    InputFailing(
        ff03,
        "Function <ff03>, parameter 'bk': <list[str]> type is not allowed "
        + "without a <str> to <list[str]> DataConverter",
    ),
]


def fp00(): ...
def fp01() -> None: ...
def fp02(input: int) -> None: ...
def fp03(input: tuple[int]) -> None: ...
def fp04(input: tuple[int, float, str]) -> None: ...
def fp11(*params: int) -> None: ...
def fp21(i: int) -> None: ...
def fp31(**kwds: float) -> None: ...
def fp41(i: float = 1) -> None: ...


passing = [
    Input(fp00, output_type=None),
    Input(fp01, output_type=type(None)),
    Input(fp02, output_type=type(None), input_types=[int]),
    Input(fp03, output_type=type(None), input_types=[int]),
    Input(fp04, output_type=type(None), input_types=[int, float, str]),
    # Input(fp11, output_type=type(None), var_arg=("params", int)),
    # Input(fp21, output_type=type(None), args=[("i", int)]),
    # Input(fp31, output_type=type(None), var_kwarg=("kwds", float)),
    # Input(fp41, output_type=type(None), kwargs=OrderedDict([("i", (float, 1))])),
]


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
        "Expected <class 'str'> but received <class 'int'> from function <dcp03>",
    ),
]


def dcp04(r: float) -> str:
    return str(r)


dcpassingruntime = [
    (dcp04, str),
]
