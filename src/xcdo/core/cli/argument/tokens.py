import re
from typing import TypeGuard

from xcdo.core.cli.exceptions import ArgSyntaxError

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
                if k in self.kwparams:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        f"Parameter '{k}' is already assigned",
                    )

                self.kwparams[k] = v
            else:
                if not self.kwparams == {}:
                    raise ArgSyntaxError(
                        self._get_pos(arg),
                        self.string,
                        "Positional parameter after keyword parameter",
                    )

                self.params.append(arg)


class FilePathToken(ArgumentToken[re.Pattern[str]]):
    pattern = re.compile(r"([^\-]\S(\S|\s)+)|(\"\S(\S|\s)+\")")
