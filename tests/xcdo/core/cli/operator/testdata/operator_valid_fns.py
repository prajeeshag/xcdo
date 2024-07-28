# type: ignore
import inspect
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Annotated, Any

from xcdo.core.cli.operator import Reader
from xcdo.core.cli.operator._Operator import _BASE_DATA_READERS


@dataclass
class _KParams:
    dtype: type = type(None)
    default: Any = inspect.Parameter.empty
    data_reader: Any = None

    def __post_init__(self):
        if self.data_reader is None and self.dtype in _BASE_DATA_READERS:
            self.data_reader = _BASE_DATA_READERS[self.dtype]


class _Params(_KParams):
    def __init__(self, name: str, dtype: type, data_reader: Any = None):
        super().__init__(dtype=dtype, data_reader=data_reader)
        self.name = name


class _VParams(_KParams):
    def __init__(self, dtype: type):
        super().__init__(dtype, default=None)


@dataclass
class _Input:
    dtypes: tuple[type, ...] = field(default_factory=tuple)
    empty: bool = True
    is_list_or_tuple: bool = False
    is_variadic: bool = False

    def __post_init__(self):
        self.len = len(self.dtypes)
        self.empty = self.empty and not bool(self.dtypes)


@dataclass
class Input:
    fn: Any
    input_types: Any = None
    args: list[_Params] = field(default_factory=list)
    var_arg: _VParams = None
    kwargs: OrderedDict[str, _KParams] = field(default_factory=OrderedDict)
    required_kwargs: OrderedDict[str, _KParams] = field(default_factory=OrderedDict)
    var_kwarg: _VParams = None
    output_type: type = type(None)

    def __post_init__(self):
        self.num_args: int = len(self.args)
        self.variadic_input = True

        if self.input_types is None:
            self.input = _Input()
        elif isinstance(self.input_types, list):
            self.input = _Input(
                dtypes=tuple(self.input_types), is_variadic=True, is_list_or_tuple=True
            )
        elif isinstance(self.input_types, tuple):
            self.input = _Input(dtypes=tuple(self.input_types), is_list_or_tuple=True)
        else:
            self.input = _Input(dtypes=tuple([self.input_types]))


def _toBool(s: str) -> bool:
    return int(s) != 0


_toBoolReader = Reader(_toBool)


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
def fp13(input: list[bool]) -> None: ...
def fp14(input: tuple[bool, ...]) -> None: ...
def fp15(input: tuple[bool, int]) -> None: ...
def fp16(i: Annotated[bool, _toBoolReader]) -> None: ...
def fp17(input: int, i: int, j: int, *args: int, k: int, m: int) -> None: ...
def fp18(
    input: int, i: int, j: int, *args: int, k: int, m: int, n: int = 1
) -> None: ...


passing = [
    Input(
        fp18,
        args=[_Params("i", int), _Params("j", int)],
        required_kwargs=OrderedDict([("k", _KParams(int)), ("m", _KParams(int))]),
        kwargs=OrderedDict([("n", _KParams(int, 1))]),
        var_arg=_VParams(int),
        input_types=int,
    ),
    Input(
        fp17,
        args=[_Params("i", int), _Params("j", int)],
        required_kwargs=OrderedDict([("k", _KParams(int)), ("m", _KParams(int))]),
        var_arg=_VParams(int),
        input_types=int,
    ),
    Input(
        fp16,
        args=[_Params("i", bool, _toBoolReader)],
    ),
    Input(fp15, input_types=(bool, int)),
    Input(fp14, input_types=[bool]),
    Input(fp13, input_types=[bool]),
    Input(
        fp12,
        kwargs=OrderedDict(
            [
                ("ik", _KParams(int, 10)),
                ("sk", _KParams(str, "hi")),
            ]
        ),
        var_kwarg=_VParams(int),
        var_arg=_VParams(str),
        args=[_Params("i", int), _Params("j", str)],
        input_types=(int, str),
        output_type=int,
    ),
    Input(
        fp11,
        kwargs=OrderedDict([("ik", _KParams(int, 1))]),
        var_kwarg=_VParams(str),
    ),
    Input(fp10, kwargs=OrderedDict([("ik", _KParams(int, 1))])),
    Input(
        fp09,
        args=[_Params("i", int), _Params("j", str)],
        var_arg=_VParams(str),
        input_types=(int, str),
    ),
    Input(fp08, args=[_Params("i", int)]),
    Input(fp07, var_arg=_VParams(int)),
    Input(fp06, input_types=[int]),
    Input(fp05, input_types=[int]),
    Input(fp04, input_types=(int, float, str)),
    Input(fp03, input_types=(int,)),
    Input(fp02, input_types=int),
    Input(fp01),
    Input(fp00),
]
