import re
from typing import TypeGuard

from xcdo.core.cli.exceptions import ArgTokenError

from .argument_token import ArgumentToken


class LeftSquareBracket(ArgumentToken[str]):
    pattern = "["


class RightSquareBracket(ArgumentToken[str]):
    pattern = "]"


class Colon(ArgumentToken[str]):
    pattern = ":"


def is_operator_token(val: object) -> TypeGuard["OperatorToken"]:
    return isinstance(val, OperatorToken)


class OperatorToken(ArgumentToken[re.Pattern[str]]):
    pattern = re.compile(r"^-(\w\w+)((\,([^=\s\,]*))|(\,(([^=\s\,]+)=([^\s\,]*))))*\,?")

    def __init__(self, string: str) -> None:
        self.string = string
        if not self.is_match(string):
            raise ValueError(f"The string '{string}' does not a match a OperatorToken")
        self._parse()

    def _get_pos(self, subarg: str) -> int:
        return self.string.index(subarg)

    def _parse(self):
        argList = list(self.string.split(","))
        self.name = argList.pop(0).lstrip("-")
        self.params: list[str] = []
        self.kwparams: dict[str, str] = {}
        for arg in argList[:]:
            if "=" in arg:
                try:
                    k, v = arg.split("=")  # Should split to 2 items
                except ValueError:
                    raise ArgTokenError(
                        self._get_pos(arg),
                        self.string,
                        "Invalid parameter",
                    )
                if not v:
                    raise ArgTokenError(
                        self._get_pos(arg),
                        self.string,
                        "Invalid parameter",
                    )
                if k in self.kwparams:
                    raise ArgTokenError(
                        self._get_pos(arg),
                        self.string,
                        f"Parameter '{k}' is already assigned",
                    )

                self.kwparams[k] = v
            else:
                if not self.kwparams == {}:
                    raise ArgTokenError(
                        self._get_pos(arg),
                        self.string,
                        "Positional parameter after keyword parameter",
                    )

                self.params.append(arg)

    def _string__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.string})"

    def __eq__(self, value: object) -> bool:
        if not is_operator_token(value):
            return False
        return value.string == self.string


class FilePathToken(ArgumentToken[re.Pattern[str]]):
    pattern = re.compile(r"([^\-]\S(\S|\s)+)|(\"\S(\S|\s)+\")")
