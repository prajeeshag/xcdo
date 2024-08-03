from typing import Hashable

from ..operator import Operator, Reader, Writer


class KeyExistsError(Exception):
    def __init__(self, key: Hashable):
        super().__init__(f"Key '{key}' already exists. Reassignment is not allowed.")
        self.key = key


class Registry[K, O]:
    def __init__(self) -> None:
        self._db: dict[K, O] = {}

    def get(self, key: K) -> O:
        return self._db[key]

    def set(self, key: K, obj: O) -> None:
        if key in self._db:
            raise KeyExistsError(key)
        self._db[key] = obj


class OperatorRegistry(Registry[str, Operator]):
    pass


class WriterRegistry(Registry[type, Writer]):
    pass


class ReaderRegistry(Registry[type, Reader]):
    pass
