import inspect
from collections import OrderedDict
from dataclasses import dataclass
from functools import cached_property
from typing import Annotated, Any, Callable, get_args, get_origin

from ..exceptions import InvalidArguments, InvalidFunction
from ._Reader import Reader
from ._utils import inspect_function, type2str


def _to_str(i: str) -> str:
    return i


def _to_int(i: str) -> int:
    return int(i)


def _to_float(i: str) -> float:
    return float(i)


# Others should pass Readers
_BASE_DATA_READERS = {
    str: Reader(_to_str),
    int: Reader(_to_int),
    float: Reader(_to_float),
}

_EMPTY = inspect.Parameter.empty


@dataclass(frozen=True)
class _Input:
    dtypes: tuple[type, ...]
    is_variadic: bool
    is_list_or_tuple: bool

    @property
    def len(self):
        return len(self.dtypes)


def _input_factory(fn: Any, ptype: Any = None) -> _Input:
    dtypes: list[type] = []
    is_variadic = False
    is_list_or_tuple = False

    pname = "input"

    if ptype is None:
        raise InvalidFunction("Should have valid type annotation", fn, pname)

    if get_origin(ptype) is tuple:
        targs = get_args(ptype)
        if Ellipsis in targs and (len(targs) != 2 or targs[0] is Ellipsis):
            raise InvalidFunction("Should have valid type annotation", fn, pname)
    if get_origin(ptype) is list and len(get_args(ptype)) != 1:
        raise InvalidFunction("Should have valid type annotation", fn, pname)
    torigin = get_origin(ptype)
    targs = get_args(ptype)
    if torigin not in (list, tuple):
        if torigin is not None:
            raise InvalidFunction(
                "Unsupported parameterized generic type for 'input'",
                fn,
            )
        dtypes = [ptype]
    elif torigin is list or (torigin is tuple and targs[-1] is Ellipsis):
        is_variadic = True
        is_list_or_tuple = True
        if get_origin(targs[0]) is not None:
            raise InvalidFunction(
                "Type of 'input' items cannot be a parameterized generic", fn
            )
        dtypes = [targs[0]]
    elif torigin is tuple:
        is_list_or_tuple = True
        for targ in targs:
            if get_origin(targ) is not None:
                raise InvalidFunction(
                    "Type of 'input' items cannot be a parameterized generic",
                    fn,
                )
            dtypes.append(targ)
    return _Input(tuple(dtypes), is_variadic, is_list_or_tuple)


@dataclass(frozen=True)
class _Param:
    name: str
    dtype: type
    default: object
    data_reader: Reader


def _param_factory(fn: Any, pname: str, ptype: Any, default: Any = _EMPTY) -> _Param:
    name = pname
    data_reader = None

    if ptype is None:
        raise InvalidFunction("Should have valid type annotation", fn, pname)

    torigin = get_origin(ptype)
    dtype = ptype
    if torigin is Annotated:
        targs = get_args(ptype)
        dtype = targs[0]
        for m in targs[1:]:
            if isinstance(m, Reader):
                data_reader = m
                break
    elif torigin is not None:
        raise InvalidFunction(
            "Parameter type cannot be a parameterized generic", fn, pname
        )
    elif ptype in _BASE_DATA_READERS:
        dtype = ptype
        data_reader = _BASE_DATA_READERS[ptype]
    if data_reader is None:
        _base_types = "(" + ",".join(map(type2str, _BASE_DATA_READERS)) + ")"
        raise InvalidFunction(
            f"Non-{_base_types} types should be annotated with a <Reader>", fn, pname
        )
    return _Param(name, dtype, default, data_reader)


@dataclass(frozen=True)
class BaseOperator:
    fn: Callable[..., object | None]
    args: tuple[_Param, ...]
    var_arg: _Param | None
    required_kwargs: tuple[_Param, ...]
    optional_kwargs: tuple[_Param, ...]
    var_kwarg: _Param | None
    output_type: type

    @cached_property
    def num_args(self) -> int:
        return len(self.args)

    def get_arg(self, n: int) -> _Param:
        if n < self.num_args:
            return self.args[n]
        elif self.var_arg:
            return self.var_arg
        raise IndexError(f"No argument at position [{n}]")

    @cached_property
    def optional_kwarg_keys(self) -> tuple[str, ...]:
        return tuple(x.name for x in self.optional_kwargs)

    @cached_property
    def required_kwarg_keys(self) -> tuple[str, ...]:
        return tuple(x.name for x in self.optional_kwargs)

    def get_kwarg(self, key: str) -> _Param:
        def get_key(obj: _Param) -> bool:
            return obj.name == key

        if key in self.optional_kwarg_keys:
            return next(filter(get_key, self.optional_kwargs))
        if key in self.required_kwarg_keys:
            return next(filter(get_key, self.required_kwargs))
        if self.var_kwarg:
            return self.var_kwarg
        raise KeyError(f"No keyword argument with key [{key}]")

    def load_kwargs(self, kwds: dict[str, str]) -> dict[str, Any]:
        self._validate_kwargs(kwds)
        pkwds: dict[str, Any] = {
            k: self.get_kwarg(k).data_reader(kwds[k]) for k in kwds
        }
        return pkwds

    def load_args(self, args: list[str]) -> tuple[Any, ...]:
        self._validate_args(args)
        pargs: tuple[Any, ...] = tuple(
            self.get_arg(i).data_reader(args[i]) for i in range(len(args))
        )
        return pargs

    def _validate_args(self, args: list[str]):
        if self.var_arg:
            if len(args) < self.num_args:
                raise InvalidArguments(
                    f"Expected at least {self.num_args} argument(s), got {len(args)}"
                )
        else:
            if len(args) != self.num_args:
                raise InvalidArguments(
                    f"Expected {self.num_args} argument(s), got {len(args)}"
                )

    def _validate_kwargs(self, kwds: dict[str, str]):
        for k in self.required_kwarg_keys:
            if k not in kwds:
                raise InvalidArguments(f"Missing required keyword argument [{k}]")

        for k in kwds:
            if (
                not self.var_kwarg
                and k not in self.required_kwarg_keys
                and k not in self.optional_kwarg_keys
            ):
                raise InvalidArguments(f"Got an unexpected keyword argument [{k}]")

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        output: object = self.fn(*args, **kwds)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Expected <{type2str(self.output_type)}> but received"
                + f" <{type2str(type(output))}> from function <{self.fn.__name__}>"
            )
        return output


@dataclass(frozen=True)
class Generator(BaseOperator):
    def __init__


@dataclass(frozen=True)
class Operator(BaseOperator):
    fn: Callable[..., object | None]
    input: _Input
    args: tuple[_Param, ...] = ()
    var_arg: _Param | None = None
    required_kwargs: tuple[_Param, ...] = ()
    optional_kwargs: tuple[_Param, ...] = ()
    var_kwarg: _Param | None = None
    output_type: type = type(None)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        output: object = self.fn(*args, **kwds)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Expected <{type2str(self.output_type)}> but received"
                + f" <{type2str(type(output))}> from function <{self.fn.__name__}>"
            )
        return output


def operator_factory(fn: Callable[..., object | None]) -> "Operator":
    _, params, output_type = inspect_function(fn)
    if output_type is None:
        output_type = type(None)

    if output_type is Any:
        raise InvalidFunction("Type 'Any' is not supported", fn)
    elif get_origin(output_type) is not None:
        raise InvalidFunction("Return type cannot be a parameterized generic type", fn)

    input = None
    args: tuple[_Param, ...] = ()
    var_arg: _Param | None = None
    required_kwargs: tuple[_Param, ...] = ()
    optional_kwargs: tuple[_Param, ...] = ()
    var_kwarg: _Param | None = None

    for i in range(len(params)):
        if params[i][1] is Any:
            raise InvalidFunction("Type 'Any' is not supported", fn, params[i][0])

        if params[i][0] == "input":
            if i > 0:
                raise InvalidFunction(
                    "If present, the 'input' parameter should be the first parameter",
                    fn,
                )
            if params[i][2] is not _EMPTY:
                raise InvalidFunction(
                    "The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter",
                    fn,
                )
            input = _input_factory(fn, params[i][1])
        elif params[i][0].startswith("**"):
            var_kwarg = _param_factory(fn, *params[i])
        elif params[i][0].startswith("*"):
            if optional_kwargs:
                raise InvalidFunction(
                    "Variadic positional arguments should be before keyword-arguments",
                    fn,
                    params[i][0],
                )
            var_arg = _param_factory(fn, *params[i])
        elif params[i][2] is _EMPTY and not var_arg:
            args.append(_param_factory(fn, *params[i]))
        elif params[i][2] is _EMPTY and var_arg:
            required_kwargs[params[i][0]] = _param_factory(fn, *params[i])
        else:
            optional_kwargs[params[i][0]] = _param_factory(fn, *params[i])
