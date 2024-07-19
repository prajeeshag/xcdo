from abc import ABC, abstractmethod
from typing import TypeVar


class Operator[I, O](ABC):
    def get_output_type(self) -> TypeVar:
        return O

    def get_input_type(self) -> TypeVar:
        return I

    @abstractmethod
    def fn(self, inputs: I) -> O:
        pass

    @abstractmethod
    def execute(self) -> O:
        pass


# DataSetTuple = tuple[DataSet, ...]


# class ChainableDataOperator(BaseOperator[DataSetTuple, DataSet]):
#     def __init__(self, children: tuple[BaseOperator[Any, DataSet], ...]) -> None:
#         self._children = children

#     @final
#     def execute(self) -> DataSet:
#         inputs = tuple(x.execute() for x in self._children)
#         return self.fn(inputs)


# class RootDataOperator(BaseOperator[DataSetTuple, None]):
#     def __init__(self, children: tuple[BaseOperator[Any, DataSet], ...]) -> None:
#         self._children = children

#     @final
#     def execute(self) -> None:
#         inputs = tuple(x.execute() for x in self._children)
#         return self.fn(inputs)


# class LeafDataOperator(BaseOperator[None, DataSet]):
#     @final
#     def execute(self) -> DataSet:
#         return self.fn(None)


# class SelectOutputOperator(BaseOperator[DataSetTuple, DataSet]):
#     def __init__(self, child: BaseOperator[Any, DataSetTuple], n: int = 0) -> None:
#         """
#         Should check value of n, for negative index as well
#         """
#         self._child = child
#         self._n = n
#         raise NotImplementedError

#     def fn(self, inputs: tuple[DataSet, ...]) -> DataSet:
#         return inputs[self._n]

#     @final
#     def execute(self) -> DataSet:
#         return super().execute()


# class SomeOperator(ChainableDataOperator):
#     def fn(self, inputs: tuple[DataSet, ...]) -> DataSet:
#         return super().fn(inputs)
