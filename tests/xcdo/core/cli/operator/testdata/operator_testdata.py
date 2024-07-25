# type: ignore
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from xcdo.core.cli.exceptions import InvalidFunction


@dataclass
class Input:
    fn: Any
    input_types: Any = None
    args: list[tuple[str, type]] = field(default_factory=list)
    var_arg: tuple[str, type | None] = ("", None)
    kwargs: OrderedDict[str, tuple[type, Any]] = field(default_factory=OrderedDict)
    var_kwarg: tuple[str, type | None] = ("", None)
    output_type: type = type(None)

    def __post_init__(self):
        self.num_args: int = len(self.args)
        self.variadic_input = True

        if self.input_types is None:
            self.num_inputs = 0
            self.variadic_input = False
        elif isinstance(self.input_types, list):
            self.variadic_input = True
            self.num_inputs = -1
        elif isinstance(self.input_types, tuple):
            self.num_inputs = len(self.input_types)  # type: ignore
            self.variadic_input = False
        else:
            self.input_types = [self.input_types]
            self.variadic_input = False
            self.num_inputs = 1


@dataclass
class InputFailing:
    fn: Any
    e: InvalidFunction


def ff00(i): ...
def ff01(ik=1): ...
def ff02(b: bool): ...
def ff03(bk: list[str] = False): ...
def ff04(input: str = ""): ...
def ff05(input: tuple[int, str, ...]) -> None: ...
def ff06(input: list[int, str]) -> None: ...
def ff07(input: tuple[int, ..., str]) -> None: ...
def ff08(input: tuple[..., str]) -> None: ...
def ff09(input: tuple[...]) -> None: ...
def ff10(input: list[int, ...]) -> None: ...


# type: ignore
failing = [
    InputFailing(
        ff10,
        InvalidFunction(
            "Should be a valid type hint",
            ff10,
            "input",
        ),
    ),
    InputFailing(
        ff09,
        InvalidFunction(
            "Should be a valid type hint",
            ff09,
            "input",
        ),
    ),
    InputFailing(
        ff08,
        InvalidFunction(
            "Should be a valid type hint",
            ff08,
            "input",
        ),
    ),
    InputFailing(
        ff07,
        InvalidFunction(
            "Should be a valid type hint",
            ff07,
            "input",
        ),
    ),
    InputFailing(
        ff00,
        InvalidFunction(
            "Parameters should have type hints",
            ff00,
            "i",
        ),
    ),
    InputFailing(
        ff01,
        InvalidFunction(
            "Parameters should have type hints",
            ff01,
            "ik",
        ),
    ),
    InputFailing(
        ff02,
        InvalidFunction(
            "Non-(str,int,float) types should use a DataReader annotation",
            ff02,
            "b",
        ),
    ),
    InputFailing(
        ff03,
        InvalidFunction(
            "Non-(str,int,float) types should use a DataReader annotation",
            ff03,
            "bk",
        ),
    ),
    InputFailing(
        ff04,
        InvalidFunction(
            "The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter",
            ff04,
        ),
    ),
    InputFailing(
        ff05,
        InvalidFunction(
            "Should be a valid type hint",
            ff05,
            "input",
        ),
    ),
    InputFailing(
        ff06,
        InvalidFunction(
            "Should be a valid type hint",
            ff06,
            "input",
        ),
    ),
]


def fp00(): ...
def fp01() -> None: ...
def fp02(input: int) -> None: ...
def fp03(input: tuple[int]) -> None: ...
def fp04(input: tuple[int, float, str]) -> None: ...
def fp05(input: list[int]) -> None: ...
def fp06(input: tuple[int, ...]) -> None: ...
def fp11(*params: int) -> None: ...
def fp21(i: int) -> None: ...
def fp31(**kwds: float) -> None: ...
def fp41(i: float = 1) -> None: ...


passing = [
    Input(fp00),
    Input(fp01),
    Input(fp02, input_types=int),
    Input(fp03, input_types=int),
    Input(fp04, input_types=(int, float, str)),
    Input(fp05, input_types=[int]),
    Input(fp06, input_types=[int]),
    # Input(fp11, output_type=type(None), var_arg=("params", int)),
    # Input(fp21, output_type=type(None), args=[("i", int)]),
    # Input(fp31, output_type=type(None), var_kwarg=("kwds", float)),
    # Input(fp41, output_type=type(None), kwargs=OrderedDict([("i", (float, 1))])),
]
