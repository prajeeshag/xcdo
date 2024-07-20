import pytest
from xcdo.core.cli.argument_tokens import (
    Colon,
    LeftSquareBracket,
    RightSquareBracket,
)


@pytest.mark.parametrize(
    "input,expected",
    [
        ["[", True],
        ["]", False],
        ["[]", False],
        ["[s]", False],
        ["s", False],
    ],
)
def test_LeftSquareBracket(input: str, expected: bool):
    assert LeftSquareBracket.match(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ["[", False],
        ["]", True],
        ["[]", False],
        ["[s]", False],
        ["s", False],
    ],
)
def test_RightSquareBracket(input: str, expected: bool):
    assert RightSquareBracket.match(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        [":", True],
        ["]", False],
        ["[:", False],
        ["[s", False],
    ],
)
def test_Colon(input: str, expected: bool):
    assert Colon.match(input) == expected
