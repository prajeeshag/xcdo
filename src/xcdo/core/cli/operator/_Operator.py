import inspect
from collections import OrderedDict
from dataclasses import dataclass
from functools import cached_property
from typing import Annotated, Any, Callable, TypeGuard, get_args, get_origin

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
    empty: bool
    dtypes: tuple[type, ...]
    is_variadic: bool
    is_list_or_tuple: bool

    @property
    def len(self):
        return len(self.dtypes)


def _input_factory(fn: Any = None, ptype: Any = None) -> _Input:
    _fn = fn
    empty = True
    dtypes: list[type] = []
    is_variadic = False
    is_list_or_tuple = False

    if fn is None:
        return _Input(empty, tuple(dtypes), is_variadic, is_list_or_tuple)

    empty = False
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
                _fn,
            )
        dtypes = [ptype]
    elif torigin is list or (torigin is tuple and targs[-1] is Ellipsis):
        is_variadic = True
        is_list_or_tuple = True
        if get_origin(targs[0]) is not None:
            raise InvalidFunction(
                "Type of 'input' items cannot be a parameterized generic", _fn
            )
        dtypes = [targs[0]]
    elif torigin is tuple:
        is_list_or_tuple = True
        for targ in targs:
            if get_origin(targ) is not None:
                raise InvalidFunction(
                    "Type of 'input' items cannot be a parameterized generic",
                    _fn,
                )
            dtypes.append(targ)
    return _Input(empty, tuple(dtypes), is_variadic, is_list_or_tuple)


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


def _is_list_tuple(x: object) -> TypeGuard[list[object] | tuple[object, ...]]:
    return isinstance(x, (list, tuple))


class Operator:
    def __init__(self, fn: Callable[..., Any]) -> None:
        self._fn = fn
        self._parse()

    def _parse(self) -> None:
        self._fname, params, self._output_type = inspect_function(self._fn)
        # Needed To maintain the original order of arguments because `input` will be removed from _params
        if self._output_type is None:
            self._output_type = type(None)

        if self._output_type is Any:
            raise InvalidFunction("Type 'Any' is not supported", self._fn)
        elif get_origin(self._output_type) is not None:
            raise InvalidFunction(
                "Return type cannot be a parameterized generic type", self._fn
            )

        self._params: list[str] = [x[0] for x in params]
        self._args: list[_Param] = []
        self._optional_kwargs: dict[str, _Param] = OrderedDict()
        self._required_kwargs: dict[str, _Param] = OrderedDict()
        self._var_arg: _Param | None = None
        self._var_kwarg: _Param | None = None
        self._input = _input_factory()

        for i in range(len(params)):
            if params[i][1] is Any:
                raise InvalidFunction(
                    "Type 'Any' is not supported", self._fn, params[i][0]
                )

            if params[i][0] == "input":
                if (
                    self._args
                    or self._optional_kwargs
                    or self._var_kwarg
                    or self._var_arg
                ):
                    raise InvalidFunction(
                        "If present, the 'input' parameter should be the first parameter",
                        self._fn,
                    )
                if params[i][2] is not _EMPTY:
                    raise InvalidFunction(
                        "The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter",
                        self._fn,
                    )
                self._input = _input_factory(self._fn, params[i][1])
            elif params[i][0].startswith("**"):
                self._var_kwarg = _param_factory(self._fn, *params[i])
            elif params[i][0].startswith("*"):
                if self._optional_kwargs:
                    raise InvalidFunction(
                        "Variadic positional arguments should be before keyword-arguments",
                        self._fn,
                        params[i][0],
                    )
                self._var_arg = _param_factory(self._fn, *params[i])
            elif params[i][2] is _EMPTY and not self._var_arg:
                self._args.append(_param_factory(self._fn, *params[i]))
            elif params[i][2] is _EMPTY and self._var_arg:
                self._required_kwargs[params[i][0]] = _param_factory(
                    self._fn, *params[i]
                )
            else:
                self._optional_kwargs[params[i][0]] = _param_factory(
                    self._fn, *params[i]
                )

    @property
    def input(self) -> _Input:
        return self._input

    @cached_property
    def num_args(self) -> int:
        return len(self._args)

    def get_arg(self, n: int) -> _Param:
        if n < self.num_args:
            return self._args[n]
        elif self.var_arg:
            return self.var_arg
        raise IndexError(f"No argument at position [{n}]")

    @property
    def var_arg(self) -> _Param | None:
        return self._var_arg

    @cached_property
    def optional_kwarg_keys(self) -> tuple[str, ...]:
        return tuple(self._optional_kwargs.keys())

    @cached_property
    def required_kwarg_keys(self) -> tuple[str, ...]:
        return tuple(self._required_kwargs.keys())

    def get_kwarg(self, key: str) -> _Param:
        if key in self._optional_kwargs:
            return self._optional_kwargs[key]
        if key in self._required_kwargs:
            return self._required_kwargs[key]
        if self.var_kwarg:
            return self.var_kwarg
        raise KeyError(f"No keyword argument with key [{key}]")

    @property
    def var_kwarg(self) -> _Param | None:
        return self._var_kwarg

    @property
    def output_type(self) -> type:
        return self._output_type

    def load_params(
        self, args: list[str], kwds: dict[str, str]
    ) -> tuple[tuple[Any, ...], dict[str, Any]]:
        self._validate_params(args, kwds)
        pargs: tuple[Any, ...] = tuple(
            self.get_arg(i).data_reader(args[i]) for i in range(len(args))
        )
        pkwds: dict[str, Any] = {
            k: self.get_kwarg(k).data_reader(kwds[k]) for k in kwds
        }
        return pargs, pkwds

    def _validate_params(self, args: list[str], kwds: dict[str, str]):
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
        output: object = self._fn(*args, **kwds)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Expected <{type2str(self.output_type)}> but received"
                + f" <{type2str(type(output))}> from function <{self._fname}>"
            )
        return output

    def _validate_input(self, input: object):
        if self.input.len > 1:
            if not _is_list_tuple(input):
                raise TypeError(
                    f"Expected a <list> or <tuple> for 'input', but got <{type2str(type(input))}>"
                )
            if self.input.len != len(input):
                raise ValueError(
                    f"'input' size mismatch: Expected ({self.input.len}), Recieved ({len(input)})"
                )
            for n in range(self.input.len):
                etype = self.input.dtypes[n]
                if not isinstance(input[n], etype):
                    raise TypeError(
                        f"Expected a <{type2str(etype)}>, but got <{type2str(type(input[n]))}> for 'input[{n}]'"
                    )
        elif self.input.len == 1:
            if _is_list_tuple(input):
                if len(input) != 1:
                    raise ValueError(
                        f"'input' size mismatch: Expected ({self.input.len}), Recieved ({len(input)})"
                    )
                etype = self.input.dtypes[0]
                if not isinstance(input[0], etype):
                    raise TypeError(
                        f"Expected a <{type2str(etype)}>, but got <{type2str(type(input[0]))}> for 'input[0]'"
                    )
            else:
                etype = self.input.dtypes[0]
                if not isinstance(input, etype):
                    raise TypeError(
                        f"Expected a <{type2str(etype)}>, but got <{type2str(type(input))}> for 'input[0]'"
                    )
