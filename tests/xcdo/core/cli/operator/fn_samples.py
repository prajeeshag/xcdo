from dataclasses import dataclass
from typing import Any


@dataclass
class Input:
    fn: Any
    num_inputs: int
    input_types: list[Any]
    num_args: int
    arg_types: list[Any]
    arg_names: list[str]
    variadic_arg_present: bool
    variadic_arg_type: Any
    kwarg_keys: tuple[str, ...]
    kwarg_types: list[Any]
    variadic_kwarg_present: bool
    variadic_kwarg_type: Any
    output_type: Any


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
    True,
    int,
    type(None),
)
