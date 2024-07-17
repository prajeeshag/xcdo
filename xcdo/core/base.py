from abc import ABC, abstractmethod
from typing import List

from xarray import Dataset


class DataSet(Dataset):
    pass


class BaseOperator(ABC):
    @abstractmethod
    def n_outputs(self) -> int:
        pass

    @abstractmethod
    def n_inputs(self) -> int:
        pass

    @abstractmethod
    def execute(self) -> DataSet | List[DataSet]:
        pass


class Operator(BaseOperator):
    def __init__(
        self,
        parent: BaseOperator,
        children: List[BaseOperator],
    ) -> None:
        self._children = children
        self._parent = parent

    @abstractmethod
    def operator_function(self, inputs: List[DataSet]):
        """
        It cannot be ze
        """

    def execute(self) -> DataSet:
        inputs = [child.execute() for child in self._children]
