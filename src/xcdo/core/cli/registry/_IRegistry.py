from abc import ABC, abstractmethod
from typing import Any


class IRegistry(ABC):
    @abstractmethod
    def get(self, key: Any) -> Any:
        """
        Returns:
            None: if `key` not present
        """
        pass
