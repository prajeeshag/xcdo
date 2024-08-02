from typing import Hashable

from xcdo.core.cli.operator._Reader import Reader

from ..operator import BaseOperator, Writer
from ._IRegistry import IRegistry


class OperatorRegistry(IRegistry):
    _db: dict[str, BaseOperator | Writer]

    def get(self, key: Hashable) -> BaseOperator | Writer:
        raise NotImplementedError

    def add(self, key: Hashable, obj: BaseOperator | Writer) -> None:
        raise NotImplementedError
