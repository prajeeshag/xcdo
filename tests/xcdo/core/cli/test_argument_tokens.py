import pytest
from xcdo.core.cli.argument_tokens import (
    Colon,
    LeftSquareBracket,
    OperatorToken,
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


@pytest.mark.parametrize(
    "input,expected",
    [
        ["-operator", True],
        ["-operator", True],
        ["-o", False],
        ["-O", False],
        ["-1", False],
        ["-operator,1", True],
        ["-operator,abc,cdf", True],
        ["-operator,abc,cdf,1", True],
        ["-operator,abc/cdf,10", True],
        ["-operator,abc/cdf.nc,10", True],
        ["-operator,abc-cdf,a/bcd/bc_d,1/3/4", True],
        ["-operator,", True],
        ["-operator,k=1", True],
        ["-operator,K=1", True],
        ["-operator,abc=123", True],
        ["-operator,abc=cdf/123/abd.nc", True],
        ["-operator,0=1", True],
        ["-operator,0abc=123", True],
        ["-operator,abc=123=cdf", False],
    ],
)
def test_OperatorToken(input: str, expected: bool):
    assert OperatorToken.match(input) == expected
