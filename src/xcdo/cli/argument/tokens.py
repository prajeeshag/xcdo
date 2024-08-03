import re
from functools import cached_property
from typing import TypeGuard

from xcdo.cli.exceptions import ArgSyntaxError

from .token import ArgumentToken


class LeftSquareBracket(ArgumentToken[str]):
    pattern = "["


class RightSquareBracket(ArgumentToken[str]):
    pattern = "]"


class Colon(ArgumentToken[str]):
    pattern = ":"


def is_operator_token(val: object) -> TypeGuard["OperatorToken"]:
    return isinstance(val, OperatorToken)


class OperatorToken(ArgumentToken[re.Pattern[str]]):
    # pattern = re.compile(r"^-(\w\w+)((\,([^=\s\,]*))|(\,(([^=\s\,]+)=([^\s\,]*))))*\,?")
    pattern = re.compile(r"^-(\w\w+)(\,(\S)*)*\,?")

    @property
    def name(self) -> str:
        return self._name

    @cached_property
    def params(self) -> list[str]:
        return self._params

    @cached_property
    def kwparams(self) -> dict[str, str]:
        return self._kwparams

    def _get_pos(self, subarg: str) -> int:
        return self.string.index(subarg)

    def _parse(self):
        argList = list(self.string.split(","))
        self._name = argList.pop(0).lstrip("-")
        self._params: list[str] = []
        self._kwparams: dict[str, str] = {}
        for arg in argList[:]:
            if "=" in arg:
                try:
                    k, v = arg.split("=")  # Should split to 2 items
                except ValueError:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        "Invalid parameter",
                    )
                if not v:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        "Invalid parameter",
                    )
                if k in self._kwparams:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        f"Parameter '{k}' is already assigned",
                    )

                self._kwparams[k] = v
            else:
                if not self._kwparams == {}:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        "Positional parameter after keyword parameter",
                    )

                self._params.append(arg)


class FilePathToken(ArgumentToken[re.Pattern[str]]):
    pattern = re.compile(r"([^\-]\S(\S|\s)+)|(\"\S(\S|\s)+\")")
