from typing import TypeGuard

from xcdo.core.cli.exceptions import ArgError


def is_arg(val: object) -> TypeGuard["OperatorArgument"]:
    return isinstance(val, OperatorArgument)


class OperatorArgument:
    def __init__(self, string: str) -> None:
        self._str = string.strip()
        self._parse()

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._str})"

    def __eq__(self, value: object) -> bool:
        if not is_arg(value):
            return False
        return value._str == self._str

    def _get_pos(self, subarg: str) -> int:
        return self._str.index(subarg)

    def _parse(self):
        argList = list(self._str.split(","))
        self._name = argList[0].lstrip("-")
        self._params: list[str] = []
        self._kwparams: dict[str, str] = {}
        for arg in argList[1:]:
            if "=" in arg:
                try:
                    k, v = arg.split("=")  # Should split to 2 items
                except ValueError:
                    raise ArgError(
                        self._get_pos(arg),
                        self._str,
                        "Invalid parameter",
                    )
                if k in self._kwparams:
                    raise ArgError(
                        self._get_pos(arg),
                        self._str,
                        f"Parameter '{k}' is already assigned",
                    )

                self._kwparams[k] = v
            else:
                self._params.append(arg)

    @property
    def name(self) -> str:
        return self._name

    @property
    def params(self) -> list[str]:
        return self._params

    @property
    def kwparams(self) -> dict[str, str]:
        return self._kwparams
