import inspect
from collections import OrderedDict
from typing import Any, Callable, get_args, get_origin

from ..exceptions import InvalidFunction
from ._utils import inspect_function, type2str

# type casting from string is trivial, others should use DataReaders
_BASE_PARAM_DATA_TYPES = [str, int, float]

_EMPTY = inspect.Parameter.empty


class Operator:
    def __init__(
        self,
        fn: Callable[..., Any],
    ) -> None:
        self._fn = fn
        self._fname: str = ""
        self._params: OrderedDict["str", tuple[type, Any]] = OrderedDict()
        self._input_types: list[type] = []
        self._is_variadic_input = False
        self._var_arg_name: str = ""
        self._var_arg_type: type = type(None)
        self._args: list[tuple[str, type]] = []
        self._var_kwarg_name: str = ""
        self._var_kwarg_type: type = type(None)
        self._kwargs: OrderedDict["str", tuple[type, Any]] = OrderedDict()
        self._parse()

    def _parse(self) -> None:
        self._fname, params, self._output_type = inspect_function(self._fn)
        # Needed To maintain the original order of arguments because `input` will be removed from _params
        if self._output_type is None:
            self._output_type = type(None)

        # TODO refactor to rules and rule checking, which is enable self documentation of rules
        for pname, ptype, dvalue in params:
            self._check_type_hints(pname, ptype)
            if pname == "input" and dvalue is not _EMPTY:
                raise InvalidFunction(
                    "The name 'input' is reserved for the `input` parameter and cannot used as an optional parameter",
                    self._fn,
                )

        for x in params:
            self._params[x[0]] = x[1:]

        var_arg = None
        var_kwarg = None
        input = None
        for i in range(len(params)):
            if params[i][0] == "input":
                if self._args or self._kwargs or var_kwarg or var_arg:
                    raise InvalidFunction(
                        "If present, the 'input' parameter should be the first parameter",
                        self._fn,
                    )
                input = params[i]
            elif params[i][0].startswith("**"):
                var_kwarg = params[i]
            elif params[i][0].startswith("*"):
                if self._kwargs:
                    raise InvalidFunction(
                        "Variadic positional arguments should be before keyword-arguments",
                        self._fn,
                        params[i][0],
                    )
                var_arg = params[i]
            elif params[i][2] is _EMPTY:
                self._args.append(params[i][0:-1])
            else:
                self._kwargs[params[i][0]] = params[i][1:]

        if input:
            self._parse_input(input)

        if var_arg:
            self._var_arg_name = var_arg[0]
            self._var_arg_type = var_arg[1]

        if var_kwarg:
            self._var_kwarg_name = var_kwarg[0]
            self._var_kwarg_type = var_kwarg[1]

    def _parse_input(self, input: Any):
        input_type = input[1]
        torigin = get_origin(input_type)
        targs = get_args(input_type)
        if torigin not in (list, tuple):
            self._input_types = [input_type]
        elif torigin is list or (torigin is tuple and targs[-1] is Ellipsis):
            self._is_variadic_input = True
            self._check_datareader(input[0], targs[0])
            self._input_types = [targs[0]]
        elif torigin is tuple:
            for subinput_type in targs:
                self._check_datareader(input[0], targs[0])
                self._input_types.append(subinput_type)

    def _check_type_hints(self, pname: str, ptype: type | None):
        if ptype is None:
            raise InvalidFunction("Parameters should have type hints", self._fn, pname)

        if get_origin(ptype) is tuple:
            targs = get_args(ptype)
            if Ellipsis in targs and (len(targs) != 2 or targs[0] is Ellipsis):
                raise InvalidFunction("Should be a valid type hint", self._fn, pname)
        if get_origin(ptype) is list and len(get_args(ptype)) != 1:
            raise InvalidFunction("Should be a valid type hint", self._fn, pname)

        if pname != "input":
            self._check_datareader(pname, ptype)

    def _check_datareader(self, pname: str, ptype: type):
        if ptype not in _BASE_PARAM_DATA_TYPES:
            _base_types = "(" + ",".join(map(type2str, _BASE_PARAM_DATA_TYPES)) + ")"
            raise InvalidFunction(
                f"Non-{_base_types} types should use a DataReader annotation",
                self._fn,
                pname,
            )

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
        return len(self._args)

    def get_arg_type(self, n: int) -> type:
        return self._args[n][1]

    def get_arg_name(self, n: int) -> str:
        return self._args[n][0]

    @property
    def var_arg(self) -> str:
        return self._var_arg_name

    @property
    def var_arg_type(self) -> type:
        return self._var_arg_type

    @property
    def kwarg_keys(self) -> tuple[str, ...]:
        return tuple(self._kwargs.keys())

    def get_kwarg_type(self, key: str) -> type:
        return self._kwargs[key][0]

    def get_kwarg_default_value(self, key: str) -> Any:
        return self._kwargs[key][1]

    @property
    def var_kwarg(self) -> str:
        return self._var_kwarg_name

    @property
    def var_kwarg_type(self) -> type:
        return self._var_kwarg_type

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
