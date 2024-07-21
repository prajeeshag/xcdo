from typing import Any

import pytest

from xcdo.core.cli.argument_parser import ArgumentParser
from xcdo.core.cli.argument_tokens import (
    FilePathToken,
    LeftSquareBracket,
    OperatorToken,
    RightSquareBracket,
)

lSqB = LeftSquareBracket("[")
rSqB = RightSquareBracket("]")
opToken = OperatorToken("-operator")
fileToken = FilePathToken("file.nc")


@pytest.fixture
def argParser():
    return ArgumentParser(
        available_tokens=[
            LeftSquareBracket,
            RightSquareBracket,
            OperatorToken,
            FilePathToken,
        ]
    )


class Test_parse:
    @pytest.mark.parametrize(
        "input,expected",
        [
            ["[ ]", [lSqB, rSqB]],
            ["[ -operator ]", [lSqB, opToken, rSqB]],
            ["[ -operator file.nc ]", [lSqB, opToken, fileToken, rSqB]],
            ["-operator file.nc", [opToken, fileToken]],
        ],
    )
    def test_closing_brackets(
        self, input: str, expected: Any, argParser: ArgumentParser
    ):
        assert argParser.parse(input.split()) == expected
