from typing import Any

import pytest
from xcdo.cli.argument.tokens import (
    FilePathToken,
    LeftSquareBracket,
    OperatorToken,
    RightSquareBracket,
    TokenParser,
)

lSqB = LeftSquareBracket("[")
rSqB = RightSquareBracket("]")
opToken = OperatorToken("-operator")
fileToken = FilePathToken("file.nc")


@pytest.fixture
def argParser():
    return TokenParser(
        available_tokens=[
            LeftSquareBracket,
            RightSquareBracket,
            OperatorToken,
            FilePathToken,
        ]
    )


class Test_tokenize:
    @pytest.mark.parametrize(
        "input,expected",
        [
            ["[ ]", [lSqB, rSqB]],
            ["[ -operator ]", [lSqB, opToken, rSqB]],
            ["[ -operator file.nc ]", [lSqB, opToken, fileToken, rSqB]],
            ["-operator file.nc", [opToken, fileToken]],
        ],
    )
    def test_valid(self, input: str, expected: Any, argParser: TokenParser):
        assert argParser.tokenize(input.split()) == expected
