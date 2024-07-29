from .argument.tokens import OperatorToken
from .registry import OperatorRegistry


class Operation:
    """
    Operation takes an OperatorToken and OperatorRegistry
    and sets the operator and its arguments. (and its children recursively
    which are again Operation)??
    """

    def __init__(self, token: OperatorToken, registry: OperatorRegistry) -> None:
        registry.get(token.name)
