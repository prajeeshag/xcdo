from dataclasses import dataclass, field
from typing import Any


@dataclass
class Input:
    fn: Any
    num_inputs: int = 0
    input_types: list[Any] = field(default_factory=list)
    num_args: int = 0
    arg_types: list[Any] = field(default_factory=list)
    arg_names: list[str] = field(default_factory=list)
    variadic_arg_present: bool = False
    variadic_arg_type: Any = None
    kwarg_keys: tuple[str, ...] = field(default_factory=tuple)
    kwarg_types: list[Any] = field(default_factory=list)
    kwarg_default_values: list[Any] = field(default_factory=list)
    variadic_kwarg_present: bool = False
    variadic_kwarg_type: Any = None
    output_type: Any = None


def fp00(): ...
def fp01() -> None: ...


passing = [
    Input(fp00, output_type=None),
    Input(fp01, output_type=type(None)),
]


def fp1(
    input: int,
    i: int,
    f: float,
    s: str,
    b: bool,
    *args: float,
    ik: int = 1,
    fk: float | int = 0.1,
    sk: str = "str",
    bk: bool = False,
    **kwargs: int,
) -> None:
    pass


fp1_param = Input(
    fp1,
    1,
    [int],
    4,
    [int, float, str, bool],
    ["i", "f", "s", "b"],
    True,
    float,
    ("ik", "fk", "sk", "bk"),
    [int, float, str, bool],
    [],
    True,
    int,
    type(None),
)
