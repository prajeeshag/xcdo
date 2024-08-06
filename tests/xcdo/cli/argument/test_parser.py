# type: ignore

import pytest
from xcdo.cli.argument.tokens import (
    FilePathToken,
    LeftSquareBracket,
    OperatorToken,
    RightSquareBracket,
    TokenParser,
)
from xcdo.cli.exceptions import ArgSyntaxError

lSqB = LeftSquareBracket()
rSqB = RightSquareBracket()
opToken = OperatorToken("operator")
fileToken = FilePathToken("file.nc")


@pytest.fixture
def argParser():
    return TokenParser(
        [
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
            ["[", lSqB],
            ["-operator", opToken],
            ["file.nc", fileToken],
        ],
    )
    def test_valid(self, input: str, expected, argParser: TokenParser):
        assert argParser.tokenize(input) == expected

    @pytest.mark.parametrize(
        "input,expected",
        [
            ["-a", ArgSyntaxError("-a", msg="Unknown pattern")],
            ["-a:sa", ArgSyntaxError("-a:sa", msg="Unknown pattern")],
            [
                "-abc,x=y=z",
                ArgSyntaxError("-abc,x=y=z", msg="Invalid parameter", pos=5),
            ],
        ],
    )
    def test_invalid(self, argParser: TokenParser, input, expected):
        with pytest.raises(ArgSyntaxError) as e:
            argParser.tokenize(input)
        assert e.value.pos == expected.pos
        assert str(e.value) == str(expected)
