from typing import Any, Type

from ..exceptions import ArgSyntaxError
from .token import ArgumentToken


class ArgumentParser:
    def __init__(self, available_tokens: list[Type[ArgumentToken[Any]]]) -> None:
        self._available_tokens = available_tokens

    def tokenize(self, argv: list[str]) -> list[ArgumentToken[Any]]:
        res: list[ArgumentToken[Any]] = []
        for arg in argv:
            argToken = self._get_valid_token(arg)
            if argToken is None:
                raise ArgSyntaxError(1, arg)
            res.append(argToken)
        return res

    def _get_valid_token(self, arg: str) -> ArgumentToken[Any] | None:
        for token in self._available_tokens:
            if token.is_match(arg):
                return token(arg)
