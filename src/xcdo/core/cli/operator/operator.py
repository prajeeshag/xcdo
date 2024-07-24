from typing import Any, Callable

from ._utils import inspect_function


class Operator:
    def __init__(
        self,
        fn: Callable[..., Any],
    ) -> None:
        self._fn = fn
        self._parse()

    def _parse(self) -> None:
        _, args, kwargs, self._output_type = inspect_function(self._fn)
        arg_names: list[str] = [x[0] for x in args]
        arg_types: list[Any] = [x[1] for x in args]
        kwarg_names = [x[0] for x in kwargs]
        kwarg_types = [x[1] for x in kwargs]
        kwarg_defaults = [x[2] for x in kwargs]

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
            self._input_types = []
            self._num_inputs = 0

    @property
    def num_inputs(self) -> int:
        return self._num_inputs

    def get_input_type(self, n: int) -> type:
        return self._input_types[n]

    @property
    def num_args(self) -> int:
        return 0

    def get_arg_type(self, n: int) -> type:
        raise NotImplementedError

    def get_arg_name(self, n: int) -> str:
        raise NotImplementedError

    @property
    def variadic_arg_present(self) -> bool:
        return False

    @property
    def variadic_arg_type(self) -> type:
        pass

    @property
    def kwarg_keys(self) -> tuple[str, ...]:
        return ()

    def get_kwarg_type(self, key: str) -> type:
        raise NotImplementedError

    def get_kwarg_default_value(self, key: str) -> Any:
        raise NotImplementedError

    @property
    def variadic_kwarg_present(self) -> bool:
        return False

    @property
    def variadic_kwarg_type(self) -> type:
        pass

    @property
    def output_type(self) -> type | None:
        return self._output_type

    def execute(self, input: tuple[Any, ...]) -> Any:
        pass
