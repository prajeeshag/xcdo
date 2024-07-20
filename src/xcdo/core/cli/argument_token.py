from abc import ABC, abstractmethod
from typing import Any, Type, final


class ArgumentMeta(type):
    def __init__(cls, name: str, bases: tuple[Any, ...], dct: dict[str, Any]):
        if cls.__name__ != "ArgumentToken":
            if "pattern" not in dct:
                raise TypeError(f"{name} class must have attribute 'pattern'")
        super().__init__(name, bases, dct)


class ArgumentToken(metaclass=ArgumentMeta):
    def __init__(self, value: str) -> None:
        self._value = value

    @property
    @final
    def value(self) -> str:
        return self._value


class AbstractTokenFactory(ABC):
    def __init__(self, token_classes: list[Type[ArgumentToken]]) -> None:
        self._token_classes = token_classes

    @abstractmethod
    def create(self, string: str) -> ArgumentToken:
        pass
