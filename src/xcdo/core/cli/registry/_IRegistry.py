from abc import ABC, abstractmethod
from typing import Any


class IRegistry(ABC):
    @abstractmethod
    def get(key: Any) -> Any:
        pass
