from typing import TypeGuard


def is_arg(val: object) -> TypeGuard["Arg"]:
    return isinstance(val, Arg)


class Arg:
    def __init__(self, string: str) -> None:
        self._str = string.strip()

    def __str__(self) -> str:
        return self._str

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self._str})"

    def __eq__(self, value: object) -> bool:
        if not is_arg(value):
            return False
        return value._str == self._str
