from ..cli.argument.tokens import OperatorToken
from ..cli.registry import OperatorRegistry


class Operations:
    """
    Operations class takes an OperatorToken and OperatorRegistry
    and sets the operator and its arguments. (and its children recursively
    which are again Operations)??
    """

    def __init__(self, token: OperatorToken, registry: OperatorRegistry) -> None:
        pass
