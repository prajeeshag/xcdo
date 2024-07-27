import inspect
from collections import OrderedDict
from typing import Annotated, Any, Callable, get_args, get_origin

from ..exceptions import InvalidFunction
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


class _Param:
    def __init__(
        self,
        fn: Callable[..., Any],
        pname: str,
        ptype: Any,
        default: Any = _EMPTY,
    ) -> None:
        self.name = pname
        self.default = default
        self.data_reader: Any = None
        if ptype is None:
            raise InvalidFunction("Should have valid type annotation", fn, pname)
        torigin = get_origin(ptype)
        if torigin is Annotated:
            targs = get_args(ptype)
            self.dtype = targs[0]
            for m in targs[1:]:
                if isinstance(m, Reader):
                    self.data_reader = m
                    break
        elif ptype in _BASE_DATA_READERS:
            self.dtype = ptype
            self.data_reader = _BASE_DATA_READERS[ptype]

        if self.data_reader is None:
            _base_types = "(" + ",".join(map(type2str, _BASE_DATA_READERS)) + ")"
            raise InvalidFunction(
                f"Non-{_base_types} types should be annotated with a <Reader>",
                fn,
                pname,
            )


class Operator:
    def __init__(
        self,
        fn: Callable[..., Any],
    ) -> None:
        self._fn = fn
        self._parse()

    def _parse(self) -> None:
        self._fname, params, self._output_type = inspect_function(self._fn)
        # Needed To maintain the original order of arguments because `input` will be removed from _params
        if self._output_type is None:
            self._output_type = type(None)

        self._params: list[str] = [x[0] for x in params]

        self._args: list[_Param] = []
        self._kwargs: dict[str, _Param] = OrderedDict()
        self._is_variadic_input = False
        self._input_types: list[type] = []
        self._var_arg: _Param | None = None
        self._var_kwarg: _Param | None = None
        for i in range(len(params)):
            if params[i][0] == "input":
                if self._args or self._kwargs or self._var_kwarg or self._var_arg:
                    raise InvalidFunction(
                        "If present, the 'input' parameter should be the first parameter",
                        self._fn,
                    )
                if params[i][2] is not _EMPTY:
                    raise InvalidFunction(
                        "The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter",
                        self._fn,
                    )
                self._parse_input(params[i])
            elif params[i][0].startswith("**"):
                self._var_kwarg = _Param(self._fn, *params[i])
            elif params[i][0].startswith("*"):
                if self._kwargs:
                    raise InvalidFunction(
                        "Variadic positional arguments should be before keyword-arguments",
                        self._fn,
                        params[i][0],
                    )
                self._var_arg = _Param(self._fn, *params[i])
            elif params[i][2] is _EMPTY:
                self._args.append(_Param(self._fn, *params[i]))
            else:
                self._kwargs[params[i][0]] = _Param(self._fn, *params[i])

    def _parse_input(self, input: Any):
        self._check_type_hints(input[0], input[1])
        input_type = input[1]
        torigin = get_origin(input_type)
        targs = get_args(input_type)
        self._is_variadic_input = False
        self._input_types: list[type] = []
        if torigin not in (list, tuple):
            self._input_types = [input_type]
        elif torigin is list or (torigin is tuple and targs[-1] is Ellipsis):
            self._is_variadic_input = True
            self._input_types = [targs[0]]
        elif torigin is tuple:
            for subinput_type in targs:
                self._input_types.append(subinput_type)

    def _check_type_hints(self, pname: str, ptype: type | None):
        if ptype is None:
            raise InvalidFunction("Should have valid type annotation", self._fn, pname)

        if get_origin(ptype) is tuple:
            targs = get_args(ptype)
            if Ellipsis in targs and (len(targs) != 2 or targs[0] is Ellipsis):
                raise InvalidFunction(
                    "Should have valid type annotation", self._fn, pname
                )
        if get_origin(ptype) is list and len(get_args(ptype)) != 1:
            raise InvalidFunction("Should have valid type annotation", self._fn, pname)

    @property
    def num_inputs(self) -> int:
        if self._is_variadic_input:
            return -1
        return len(self._input_types)

    @property
    def is_variadic_input(self) -> bool:
        return self._is_variadic_input

    def get_input_type(self, n: int = 0) -> type:
        return self._input_types[n]

    @property
    def num_args(self) -> int:
        print(self._args)
        return len(self._args)

    def get_arg(self, n: int) -> _Param:
        return self._args[n]

    @property
    def var_arg(self) -> _Param | None:
        return self._var_arg

    @property
    def kwarg_keys(self) -> tuple[str, ...]:
        return tuple(self._kwargs.keys())

    def get_kwarg(self, key: str) -> _Param:
        return self._kwargs[key]

    @property
    def var_kwarg(self) -> _Param | None:
        return self._var_kwarg

    @property
    def output_type(self) -> type:
        return self._output_type

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        output: object = self._fn(*args, **kwds)
        if not isinstance(output, self.output_type):
            raise TypeError(
                f"Expected <{type2str(self.output_type)}> but received"
                + f" <{type2str(type(output))}> from function <{self._fname}>"
            )
        return output
