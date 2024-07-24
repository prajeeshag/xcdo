from collections import OrderedDict
from typing import Any, Callable

from ._utils import inspect_function

# type casting from string is trivial, others should use DataConverter
_BASE_DATA_TYPES = [str, int, float]


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
        _, args, kwargs, self._output_type = inspect_function(self._fn)
        arg_names: list[str] = [x[0] for x in args]
        arg_types: list[Any] = [x[1] for x in args]
        kwarg_names = [x[0] for x in kwargs]
        kwarg_types = [x[1] for x in kwargs]
        kwarg_defaults = [x[2] for x in kwargs]

        self._parse_input(arg_names, arg_types)

        self._parge_var_arg(arg_names, arg_types)
        self._args = list(zip(arg_names, arg_types))
        self._parge_var_kwarg(kwarg_names, kwarg_types, kwarg_defaults)
        self._kwargs = OrderedDict(
            list(zip(kwarg_names, tuple(zip(kwarg_types, kwarg_defaults))))
        )

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

    def _parge_var_arg(self, arg_names: list[str], arg_types: list[Any]) -> None:
        self._var_arg_name: str = ""
        self._var_arg_type: type | None = None
        for i in range(len(arg_names)):
            if arg_names[i].startswith("*"):
                self._var_arg_name = arg_names.pop(i).lstrip("*")
                self._var_arg_type = arg_types.pop(i)
                return

    def _parse_input(self, arg_names: list[str], arg_types: list[Any]):
        try:
            index = arg_names.index("input")
            arg_names.pop(index)
            input_type = arg_types.pop(index)

            if not hasattr(input_type, "__origin__"):
                self._input_types = [input_type]
                self._num_inputs = 1
            elif input_type.__origin__ is list:
                pass
            elif input_type.__origin__ is tuple:
                pass
        except ValueError:
            pass

    @property
    def num_inputs(self) -> int:
        return self._num_inputs

    def get_input_type(self, n: int) -> type:
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
    def var_arg_type(self) -> type | None:
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
