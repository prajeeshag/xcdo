import re
from functools import cached_property
from typing import Any, Type, TypeGuard

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
                        pos=self._get_pos(arg),
                        msg="Invalid parameter",
                    )
                if not v:
                    raise ArgSyntaxError(
                        pos=self._get_pos(arg),
                        msg="Invalid parameter",
                    )
                if k in self._kwparams:
                    raise ArgSyntaxError(
                        pos=self._get_pos(arg),
                        msg="Parameter already assigned",
                    )

                self._kwparams[k] = v
            else:
                if not self._kwparams == {}:
                    raise ArgSyntaxError(
                        pos=self._get_pos(arg),
                        msg="Positional parameter after keyword parameter is not allowed",
                    )

                self._params.append(arg)


class FilePathToken(ArgumentToken[re.Pattern[str]]):
    pattern = re.compile(r"([^\-]\S(\S|\s)+)")


class TokenParser:
    def __init__(self, available_tokens: list[Type[ArgumentToken[Any]]]) -> None:
        self._available_tokens = available_tokens

    def tokenize(self, arg: str) -> ArgumentToken[str] | ArgumentToken[re.Pattern[str]]:
        for token in self._available_tokens:
            if token.is_match(arg):
                return token(arg)
        raise ArgSyntaxError(msg="Unknown pattern")
