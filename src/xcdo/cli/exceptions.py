from typing import Any, Callable


class ArgSyntaxError(Exception):
    def __init__(self, token: str, pos: int = 0, msg: str = "") -> None:
        self.pos = pos
        self.token = token
        args = ()
        if msg:
            args = (msg,)
        super().__init__(*args)


class OperatorNotFound(Exception):
    def __init__(self, operator: str) -> None:
        self.operator = operator


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
