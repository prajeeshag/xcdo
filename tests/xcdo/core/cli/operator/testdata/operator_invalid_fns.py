# type: ignore
import sys
from dataclasses import dataclass
from typing import Any, Callable

from xcdo.core.cli.exceptions import InvalidFunction

from tests.xcdo.core.cli.operator.testdata.utils import list_functions

from .utils import e_args


@dataclass
class InputFailing:
    fn: Any
    e: InvalidFunction


def ff00(i):
    """
    Should have valid type annotation
    i
    """


def ff01(ik=1):
    """
    Should have valid type annotation
    ik
    """


def ff02(b: bool):
    """
    Non-(str,int,float) types should be annotated with a <Reader>
    b
    """


def ff03(bk: bool = False):
    """
    Non-(str,int,float) types should be annotated with a <Reader>
    bk
    """


def ff04(input: str = ""):
    """
    The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter
    """


def ff05(input: tuple[int, str, ...]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff06(input: list[int, str]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff07(input: tuple[int, ..., str]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff08(input: tuple[..., str]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff09(input: tuple[...]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff10(input: list[int, ...]) -> None:
    """
    Should have valid type annotation
    input
    """


def ff13(*b: bool):
    """
    Non-(str,int,float) types should be annotated with a <Reader>
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


def ff16(i: list[str]) -> int:
    """
    Parameter type cannot be a parameterized generic
    i
    """


def ff17(j: int, k: dict[str, str] = {"k": "j"}) -> int:
    """
    Parameter type cannot be a parameterized generic
    k
    """


def ff18(j: int, *k: dict[str, str]) -> int:
    """
    Parameter type cannot be a parameterized generic
    *k
    """


def ff19(j: int, **k: dict[str, str]) -> int:
    """
    Parameter type cannot be a parameterized generic
    **k
    """


def ff20(input: list[tuple[str, ...]]) -> int:
    """
    Type of 'input' items cannot be a parameterized generic
    """


def ff21(input: tuple[list[str]]) -> int:
    """
    Type of 'input' items cannot be a parameterized generic
    """


def ff22(input: Callable[str, str]) -> int:
    """
    Unsupported parameterized generic type for 'input'
    """


def ff23() -> list[int]:
    """
    Return type cannot be a parameterized generic type
    """


def ff24() -> Any:
    """
    Type 'Any' is not supported
    """


def ff25(i: Any):
    """
    Type 'Any' is not supported
    i
    """


def ff26(ik: Any = 1):
    """
    Type 'Any' is not supported
    ik
    """


def ff27(input: Any):
    """
    Type 'Any' is not supported
    input
    """


def ff28(*i: Any):
    """
    Type 'Any' is not supported
    *i
    """


def ff29(**i: Any):
    """
    Type 'Any' is not supported
    **i
    """


def ff30(input: None) -> int:
    """
    Parameter cannot be type 'None'
    input
    """


def ff31(input: list[None]) -> int:
    """
    Input cannot be type 'None'
    """


def ff32(input: tuple[None, ...]) -> int:
    """
    Input cannot be type 'None'
    """


_current_module = sys.modules[__name__]
ff_fns = list_functions(_current_module, "ff")
failing = [InputFailing(fn, InvalidFunction(*e_args(fn))) for fn in ff_fns]
