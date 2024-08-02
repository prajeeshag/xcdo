from abc import ABC, abstractmethod
from typing import Any, Hashable

from ..operator import BaseOperator, Reader, Writer


class IRegistry(ABC):
    @abstractmethod
    def get(self, key: Hashable) -> BaseOperator | Writer | Reader:
        """
        Returns:
            None: if `key` not present
        """
        pass

    @abstractmethod
    def add(self, key: Hashable, obj: Any) -> None:
        """
        Raises:
            EntryExistError if key already exist
        """
        pass
