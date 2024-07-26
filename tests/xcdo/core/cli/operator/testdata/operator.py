# type: ignore
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from xcdo.core.cli.exceptions import InvalidFunction

from .utils import e_args


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
def ff11(input: list[bool]) -> None: ...
def ff12(input: tuple[bool, ...]) -> None:
    """
    Non-(str,int,float) types should use a DataReader annotation
    input
    """


def ff13(*b: list[str]):
    """
    Non-(str,int,float) types should use a DataReader annotation
    *b
    """


def ff14(ik: int = 10, *params: str) -> int:
    """
    Variadic positional arguments should be before keyword-arguments
    *params
    """


def ff15(ik: int, input: str, *params: str) -> int:
    """
    If present, the 'input' parameter should be the first parameter
    """


failing = [
    InputFailing(ff15, InvalidFunction(*e_args(ff15))),
    InputFailing(ff14, InvalidFunction(*e_args(ff14))),
    InputFailing(ff13, InvalidFunction(*e_args(ff13))),
    InputFailing(ff12, InvalidFunction(*e_args(ff12))),
    InputFailing(
        ff11,
        InvalidFunction(
            "Non-(str,int,float) types should use a DataReader annotation",
            ff11,
            "input",
        ),
    ),
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


@dataclass
class Input:
    fn: Any
    input_types: Any = None
    args: list[tuple[str, type]] = field(default_factory=list)
    var_arg: tuple[str, type] = ("", type(None))
    kwargs: OrderedDict[str, tuple[type, Any]] = field(default_factory=OrderedDict)
    var_kwarg: tuple[str, type] = ("", type(None))
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


def fp00(): ...
def fp01() -> None: ...
def fp02(input: int) -> None: ...
def fp03(input: tuple[int]) -> None: ...
def fp04(input: tuple[int, float, str]) -> None: ...
def fp05(input: list[int]) -> None: ...
def fp06(input: tuple[int, ...]) -> None: ...
def fp07(*params: int) -> None: ...
def fp08(i: int) -> None: ...
def fp09(input: tuple[int, str], i: int, j: str, *params: str) -> None: ...
def fp10(ik: int = 1) -> None: ...
def fp11(ik: int = 1, **kwds: str) -> None: ...
def fp12(
    input: tuple[int, str],
    i: int,
    j: str,
    *params: str,
    ik: int = 10,
    sk: str = "hi",
    **kwargs: int,
) -> int: ...


passing = [
    Input(
        fp12,
        kwargs=OrderedDict([("ik", (int, 10)), ("sk", (str, "hi"))]),
        var_kwarg=("**kwargs", int),
        var_arg=("*params", str),
        args=[("i", int), ("j", str)],
        input_types=(int, str),
        output_type=int,
    ),
    Input(
        fp11,
        kwargs=OrderedDict([("ik", (int, 1))]),
        var_kwarg=("**kwds", str),
    ),
    Input(
        fp10,
        kwargs=OrderedDict([("ik", (int, 1))]),
    ),
    Input(
        fp09,
        args=[("i", int), ("j", str)],
        var_arg=("*params", str),
        input_types=(int, str),
    ),
    Input(fp08, args=[("i", int)]),
    Input(fp07, var_arg=("*params", int)),
    Input(fp06, input_types=[int]),
    Input(fp05, input_types=[int]),
    Input(fp04, input_types=(int, float, str)),
    Input(fp03, input_types=int),
    Input(fp02, input_types=int),
    Input(fp01),
    Input(fp00),
]
