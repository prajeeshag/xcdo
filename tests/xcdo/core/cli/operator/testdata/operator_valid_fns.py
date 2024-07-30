# type: ignore
from typing import Annotated

from xcdo.core.cli.operator import Generator as Ge
from xcdo.core.cli.operator import Operator as Op
from xcdo.core.cli.operator import Reader
from xcdo.core.cli.operator._Operator import _BASE_DATA_READERS as dR
from xcdo.core.cli.operator._Operator import _Input as I
from xcdo.core.cli.operator._Operator import _Param as P


def _toBool(s: str) -> bool:
    return int(s) != 0


_toBoolReader = Reader(_toBool)

passing = []


def fp00(): ...


passing += [Ge(fp00)]


def fp01() -> None: ...


passing += [Ge(fp01)]


def fp02(input: int) -> None: ...


passing += [Op(fp02, input=I((int,), False, False))]


def fp03(input: tuple[int]) -> None: ...


passing += [Op(fp03, input=I((int,), False, True))]


def fp04(input: tuple[int, float, str]) -> None: ...


passing += [Op(fp04, input=I((int, float, str), False, True))]


def fp05(input: list[int]) -> None: ...


passing += [Op(fp05, input=I((int,), True, True))]


def fp06(input: tuple[int, ...]) -> None: ...


passing += [Op(fp06, input=I((int,), True, True))]


def fp07(*params: int) -> None: ...


passing += [Ge(fp07, var_arg=P("*params", int, dR[int]))]


def fp08(i: int) -> None: ...


passing += [Ge(fp08, args=(P("i", int, dR[int]),))]


def fp09(input: tuple[int, str], i: int, j: str, *params: str) -> None: ...


passing += [
    Op(
        fp09,
        args=(
            P("i", int, dR[int]),
            P("j", str, dR[str]),
        ),
        var_arg=P("*params", str, dR[str]),
        input=I((int, str), False, True),
    )
]


def fp10(ik: int = 1) -> None: ...


passing += [Ge(fp10, optional_kwargs=(P("ik", int, dR[int], 1),))]


def fp11(ik: int = 1, **kwds: str) -> None: ...


passing += [
    Ge(
        fp11,
        optional_kwargs=(P("ik", int, dR[int], 1),),
        var_kwarg=P("**kwds", str, dR[str]),
    )
]


def fp12(
    input: tuple[int, str],
    i: int,
    j: str,
    *params: str,
    ik: int = 10,
    sk: str = "hi",
    **kwargs: int,
) -> int: ...


passing += [
    Op(
        fp12,
        (P("i", int, dR[int]), P("j", str, dR[str])),
        P("*params", str, dR[str]),
        (),
        (
            P("ik", int, dR[int], 10),
            P("sk", str, dR[str], "hi"),
        ),
        P("**kwargs", int, dR[int]),
        int,
        input=I((int, str), False, True),
    )
]


def fp13(input: list[bool]) -> None: ...


passing += [Op(fp13, input=I((bool,), True, True))]


def fp14(input: tuple[bool, ...]) -> None: ...


passing += [Op(fp14, input=I((bool,), True, True))]


def fp15(input: tuple[bool, int]) -> None: ...


passing += [Op(fp15, input=I((bool, int), False, True))]


def fp16(i: Annotated[bool, _toBoolReader]) -> None: ...


passing += [Ge(fp16, (P("i", bool, _toBoolReader),))]


def fp17(input: int, i: int, j: int, *args: int, k: int, m: int) -> None: ...


passing += [
    Op(
        fp17,
        (P("i", int, dR[int]), P("j", int, dR[int])),
        P("*args", int, dR[int]),
        (P("k", int, dR[int]), P("m", int, dR[int])),
        input=I((int,), False, False),
    )
]


def fp18(
    input: int, i: int, j: int, *args: int, k: int, m: int, n: int = 1
) -> None: ...


passing += [
    Op(
        fp18,
        args=(P("i", int, dR[int]), P("j", int, dR[int])),
        required_kwargs=(P("k", int, dR[int]), P("m", int, dR[int])),
        optional_kwargs=(P("n", int, dR[int], 1),),
        var_arg=P("*args", int, dR[int]),
        input=I((int,), False, False),
    ),
]
