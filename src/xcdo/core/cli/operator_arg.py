from .arg import Arg
from .exceptions import ArgError


class OperatorArg(Arg):
    def __init__(self, string: str) -> None:
        super().__init__(string)
        self._parse()

    def get_pos(self, subarg: str) -> int:
        return self._str.index(subarg)

    def _parse(self):
        argList = list(self._str.split(","))
        self._name = argList[0].lstrip("-")
        self._params: list[str] = []
        self._kwparams: dict[str, str] = {}
        for arg in argList[1:]:
            if "=" in arg:
                try:
                    k, v = arg.split("=")  # Should split to 2 items
                except ValueError:
                    raise ArgError(
                        self.get_pos(arg),
                        self._str,
                        "Invalid parameter",
                    )
                if k in self._kwparams:
                    raise ArgError(
                        self.get_pos(arg),
                        self._str,
                        f"Parameter '{k}' is already assigned",
                    )

                self._kwparams[k] = v
            else:
                self._params.append(arg)

    @property
    def name(self) -> str:
        return self._name

    @property
    def params(self) -> list[str]:
        return self._params

    @property
    def kwparams(self) -> dict[str, str]:
        return self._kwparams
