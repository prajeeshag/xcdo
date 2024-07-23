# type: ignore
import pytest
from xcdo.core.cli.exceptions import OperatorDefError
from xcdo.core.cli.operator._utils import inspect_function


def passing1(
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


def passing2(i, f, s, b, ik=1, *args, fk=0.1, sk="str", bk=False, **kwargs):
    pass


@pytest.mark.parametrize(
    "input,expected",
    [
        [
            passing1,
            (
                "passing1",
                [
                    ("i", int),
                    ("f", float),
                    ("s", str),
                    ("b", bool),
                    ("*args", float),
                ],
                [
                    ("ik", int, 1),
                    ("fk", float | int, 0.1),
                    ("sk", str, "str"),
                    ("bk", bool, False),
                    ("**kwargs", int, None),
                ],
                type(None),
            ),
        ],
        [
            passing2,
            (
                "passing2",
                [
                    ("i", None),
                    ("f", None),
                    ("s", None),
                    ("b", None),
                    ("*args", None),
                ],
                [
                    ("ik", None, 1),
                    ("fk", None, 0.1),
                    ("sk", None, "str"),
                    ("bk", None, False),
                    ("**kwargs", None, None),
                ],
                None,
            ),
        ],
    ],
)
def test_passing(input, expected):
    assert inspect_function(input) == expected
