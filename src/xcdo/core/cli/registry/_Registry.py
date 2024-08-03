from abc import ABC, abstractmethod
from typing import Hashable


class KeyExistsError(Exception):
    def __init__(self, key: Hashable):
        super().__init__(f"Key '{key}' already exists. Reassignment is not allowed.")
        self.key = key


class IRegistry(ABC):
    @abstractmethod
    def get(self, key: Hashable) -> object:
        """
        Raises:
            KeyError if 'key' not found
        """
        pass

    @abstractmethod
    def set(self, key: Hashable, obj: object) -> None:
        """
        Raises:
            KeyExistsError if key already exist
        """
        pass


class Registry(IRegistry):
    def __init__(self) -> None:
        self._db: dict[Hashable, object] = {}

    def get(self, key: Hashable) -> object:
        return self._db[key]

    def set(self, key: Hashable, obj: object) -> None:
        if key in self._db:
            raise KeyExistsError(key)
        self._db[key] = obj
