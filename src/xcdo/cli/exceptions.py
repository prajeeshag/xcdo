from typing import Any, Callable


class SyntaxError(Exception):
    def __init__(self, pos: int = 0, index: int = 0, msg: str = "") -> None:
        self.pos = pos
        self.index = index
        args = ()
        if msg:
            args = (msg,)
        super().__init__(*args)


class OperatorNotFound(Exception):
    def __init__(self, operator: str, index: int = -1) -> None:
        self.operator = operator
        self.index = index


class InvalidFunction(Exception):
    def __init__(
        self,
        msg: object,
        fn: Callable[..., Any] | None = None,
        pname: str = "",
    ) -> None:
        self.fn = fn
        self.pname = pname
        super().__init__(msg)


class InvalidArguments(Exception):
    pass
