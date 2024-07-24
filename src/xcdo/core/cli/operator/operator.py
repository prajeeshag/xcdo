from collections import OrderedDict
from typing import Any, Callable

from ..exceptions import InvalidDefinition
from ._utils import inspect_function, type2str

# type casting from string is trivial, others should use DataConverter
_BASE_PARAM_DATA_TYPES = [str, int, float]


class Operator:
    def __init__(
        self,
        fn: Callable[..., Any],
    ) -> None:
        self._fn = fn
        self._input_types: list[type] = []
        self._num_inputs: int = 0
        self._parse()

    def _parse(self) -> None:
        (
            self._name,
            self._params,
            self._kwparams,
            self._output_type,
        ) = inspect_function(self._fn)
        # this is needed because `input` will be removed from _params, so to maintain the orginal order of arguments
        self._arg_keys = [x[0] for x in self._params]

        for pname, ptype in self._params:
            if ptype is None:
                raise InvalidDefinition(
                    f"Function <{self._name}>: missing type hint for parameter '{pname}'"
                )
            if pname != "input" and ptype not in _BASE_PARAM_DATA_TYPES:
                raise InvalidDefinition(
                    f"Function <{self._name}>, parameter '{pname}': "
                    + f"<{type2str(ptype)}> type is not allowed without a <str> to "
                    + f"<{type2str(ptype)}> DataConverter"
                )
        for pname, ptype, _ in self._kwparams:
            if ptype is None:
                raise InvalidDefinition(
                    f"Function <{self._name}>: missing type hint for parameter '{pname}'"
                )
            if ptype not in _BASE_PARAM_DATA_TYPES:
                raise InvalidDefinition(
                    f"Function <{self._name}>, parameter '{pname}': "
                    + f"<{type2str(ptype)}> type is not allowed without a <str> to "
                    + f"<{type2str(ptype)}> DataConverter"
                )

        # self._parse_input()

        # self._parse_var_arg()

        # self._parge_var_arg(arg_names, arg_types)
        # self._args = list(zip(arg_names, arg_types))
        # self._parge_var_kwarg(kwarg_names, kwarg_types, kwarg_defaults)
        # self._kwargs = OrderedDict(
        #    list(zip(kwarg_names, tuple(zip(kwarg_types, kwarg_defaults))))
        # )

    def _parge_var_kwarg(
        self,
        kwarg_names: list[str],
        kwarg_types: list[Any],
        kwarg_defaults: list[Any],
    ) -> None:
        self._var_kwarg_name: str = ""
        self._var_kwarg_type: type | None = None
        for i in range(len(kwarg_names)):
            if kwarg_names[i].startswith("**"):
                self._var_kwarg_name = kwarg_names.pop(i).lstrip("**")
                self._var_kwarg_type = kwarg_types.pop(i)
                kwarg_defaults.pop(i)
                return

    def _parse_var_arg(self):
        self._var_arg_name: str = ""
        self._var_arg_type: type | None = None
        var_arg = None
        for i in range(len(self._params)):
            if self._params[i][0].startswith("*"):
                var_arg = self._params.pop(i)
                break
        if var_arg:
            self._var_arg_name = var_arg[0]
            self._var_arg_type = var_arg[1]

    def _parse_input(self):
        self._input_types = []
        self._num_inputs = 0
        input = None
        for i in range(len(self._params)):
            if self._params[i][0] == "input":
                input = self._params.pop(i)
                break
        if input:
            input_type = input[1]
            if not hasattr(input_type, "__origin__"):
                self._input_types = [input_type]
                self._num_inputs = 1
            elif input_type.__origin__ is list:
                raise NotImplementedError
            elif input_type.__origin__ is tuple:
                raise NotImplementedError

    @property
    def num_inputs(self) -> int:
        return self._num_inputs

    def get_input_type(self, n: int) -> type:
        return self._input_types[n]

    @property
    def num_args(self) -> int:
        return len(self._params)

    def get_arg_type(self, n: int) -> type:
        return self._params[n][1]

    def get_arg_name(self, n: int) -> str:
        return self._params[n][0]

    @property
    def var_arg(self) -> str:
        return self._var_arg_name

    @property
    def var_arg_type(self) -> type | None:
        return self._var_arg_type

    @property
    def kwarg_keys(self) -> tuple[str, ...]:
        return tuple(self._kwparams.keys())

    def get_kwarg_type(self, key: str) -> type:
        return self._kwparams[key][0]

    def get_kwarg_default_value(self, key: str) -> Any:
        return self._kwparams[key][1]

    @property
    def var_kwarg(self) -> str:
        return self._var_kwarg_name

    @property
    def var_kwarg_type(self) -> type | None:
        return self._var_kwarg_type

    @property
    def output_type(self) -> type | None:
        return self._output_type

    def is_reader(self) -> bool:
        raise NotImplementedError

    def is_writer(self) -> bool:
        raise NotImplementedError

    def execute(self, input: tuple[Any, ...]) -> Any:
        pass
