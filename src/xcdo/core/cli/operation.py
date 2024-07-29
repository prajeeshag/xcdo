from typing import TypeAlias

from .operator import Operator

OperationType: TypeAlias = "Operation"


class Operation:
    """
    Operation takes an Operator, args, kwargs and optionally child Operations
    """

    def __init__(
        self,
        operator: Operator,
        args: list[object],
        kwargs: dict[str, object],
        inputs: list[OperationType],
    ) -> None:
        pass
