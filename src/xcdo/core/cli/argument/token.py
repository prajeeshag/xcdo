import re
from abc import ABC, abstractmethod
from typing import Any, Type


class ArgumentMeta(type):
    def __init__(cls, name: str, bases: tuple[Any, ...], dct: dict[str, Any]):
        if cls.__name__ != "ArgumentToken":
            if "pattern" not in dct:
                raise TypeError(f"{name} class must have attribute 'pattern'")
            if not isinstance(dct["pattern"], (re.Pattern, str)):
                raise TypeError(
                    f"{name} class attribute 'pattern' should be a <str> or re.Pattern object"
                )
        super().__init__(name, bases, dct)


class ArgumentToken[S: (re.Pattern[str], str)](metaclass=ArgumentMeta):
    pattern: S

    @classmethod
    def is_match(cls, string: str):
        if isinstance(cls.pattern, re.Pattern):
            return bool(cls.pattern.fullmatch(string))
        else:
            return string == cls.pattern

    def __init__(self, string: str) -> None:
        self.string = string
        if not self.is_match(string):
            raise ValueError(f"The string '{string}' does not a match a OperatorToken")
        self._parse()

    def _parse(self):
        pass

    def _string__(self) -> str:
        return self.string

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.string})"

    def __eq__(self, value: object) -> bool:
        if type(value) is type(self) and self.string == value.string:
            return True
        return False


class AbstractTokenFactory(ABC):
    def __init__(self, token_classes: list[Type[ArgumentToken[Any]]]) -> None:
        self._token_classes = token_classes

    @abstractmethod
    def create(self, string: str) -> ArgumentToken[Any]:
        pass
