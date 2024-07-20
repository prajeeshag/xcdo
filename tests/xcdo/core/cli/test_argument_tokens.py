import pytest
from xcdo.core.cli.argument_tokens import LeftSquareBracket


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
