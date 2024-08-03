import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Type, TypeGuard

from xcdo.cli.exceptions import ArgSyntaxError


class ArgumentToken(ABC):
    @classmethod
    @abstractmethod
    def factory(cls, string: str) -> "ArgumentToken | None":
        raise NotImplementedError


@dataclass(frozen=True)
class LeftSquareBracket(ArgumentToken):
    @classmethod
    def factory(cls, string: str) -> ArgumentToken | None:
        if string == "[":
            return cls()


@dataclass(frozen=True)
class RightSquareBracket(ArgumentToken):
    @classmethod
    def factory(cls, string: str) -> ArgumentToken | None:
        if string == "]":
            return cls()


@dataclass(frozen=True)
class Colon(ArgumentToken):
    @classmethod
    def factory(cls, string: str) -> ArgumentToken | None:
        if string == ":":
            return cls()


def is_operator_token(val: object) -> TypeGuard["OperatorToken"]:
    return isinstance(val, OperatorToken)


@dataclass(frozen=True)
class OperatorToken(ArgumentToken):
    name: str
    params: tuple[str, ...] = ()
    kwparams: tuple[tuple[str, str], ...] = ()

    @classmethod
    def factory(cls, string: str) -> ArgumentToken | None:
        pattern = re.compile(r"^-(\w\w+)(\,(\S)*)*\,?")
        if not bool(pattern.fullmatch(string)):
            return None

        argList = list(string.split(","))
        name = argList.pop(0).lstrip("-")
        params: list[str] = []
        kwparams: list[tuple[str, str]] = []
        for arg in argList[:]:
            if "=" in arg:
                try:
                    k, v = arg.split("=")  # Should split to 2 items
                except ValueError:
                    raise ArgSyntaxError(pos=string.index(arg), msg="Invalid parameter")
                if not v:
                    raise ArgSyntaxError(pos=string.index(arg), msg="Invalid parameter")
                if k in dict(kwparams):
                    raise ArgSyntaxError(
                        pos=string.index(arg), msg="Parameter already assigned"
                    )

                kwparams.append((k, v))
            else:
                if len(kwparams) != 0:
                    raise ArgSyntaxError(
                        pos=string.index(arg),
                        msg="Positional parameter after keyword parameter is not allowed",
                    )

                params.append(arg)
        return OperatorToken(name, tuple(params), tuple(kwparams))


@dataclass(frozen=True)
class FilePathToken(ArgumentToken):
    path: str

    @classmethod
    def factory(cls, string: str) -> ArgumentToken | None:
        pattern = re.compile(r"([^\-]\S(\S|\s)+)")
        if bool(pattern.fullmatch(string)):
            return FilePathToken(string)


class TokenParser:
    def __init__(self, token_classes: list[Type[ArgumentToken]]) -> None:
        self._token_classes = token_classes

    def tokenize(self, arg: str) -> ArgumentToken:
        for token_class in self._token_classes:
            token = token_class.factory(arg)
            if token is not None:
                return token
        raise ArgSyntaxError(msg="Unknown pattern")
