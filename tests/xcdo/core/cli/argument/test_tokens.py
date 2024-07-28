from typing import Any

import pytest
from xcdo.core.cli.argument.tokens import (
    Colon,
    FilePathToken,
    LeftSquareBracket,
    OperatorToken,
    RightSquareBracket,
)
from xcdo.core.cli.exceptions import ArgSyntaxError


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
    assert LeftSquareBracket.is_match(input) == expected


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
    assert RightSquareBracket.is_match(input) == expected


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
    assert Colon.is_match(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ["-operator", True],
        ["-opeRator", True],
        ["-ope_Rator", True],
        ["-o", False],
        ["-O", False],
        ["-1", False],
        ["--operator", False],
        ["operator", False],
        ["-operator,1", True],
        ["-operator,abc,cdf", True],
        ["-operator,abc,cdf,1", True],
        ["-operator,abc/cdf,10", True],
        ["-operator,abc/cdf.nc,10", True],
        ["-ope_rator,abc-cdf,a/bcd/bc_d,1/3/4", True],
        ["-operator,", True],
        ["-operator,k=1", True],
        ["-operator,K=1", True],
        ["-operator,abc=123", True],
        ["-operator,abc=cdf/123/abd.nc", True],
        ["-operator,0=1,a=b,x=y", True],
        ["-operator,b2,c3,d4,0=1,a=b,x=y", True],
        ["-operator,0abc=123", True],
        ["-singleOptionalParam,p1,,p3", True],
        # These 2 errors will be captured while parsing
        ["-operator,abc=123=cdf", True],
        ["-operator,abc=123,dcf", True],
        ["-operator,abc=", True],
    ],
)
def test_OperatorTokenPattern(input: str, expected: bool):
    assert OperatorToken.is_match(input) == expected


class Test_OperatorToken:
    parameters: Any = (
        ("-simple,k1=v1=v2", (8, "Invalid parameter")),
        ("-simple,k1=v1,k1=v2", (14, "Parameter 'k1' is already assigned")),
        ("-simple,k2=v1,k1=v2,k2=v2", (20, "Parameter 'k2' is already assigned")),
        ["-operator,abc=", (10, "Invalid parameter")],
        [
            "-operator,abc=dfg,123",
            (18, "Positional parameter after keyword parameter"),
        ],
    )

    @pytest.mark.parametrize("string,expected", parameters)
    def test_invalid(self, string: str, expected: Any):
        with pytest.raises(ArgSyntaxError) as result:
            OperatorToken(string)

        assert result.value.pos == expected[0]
        assert result.value.string == string
        assert str(result.value) == expected[1]

    class Test_valid:
        parameters: Any = (
            (
                "-simple",
                ("simple", (), {}),
            ),
            (
                "-singleParam,p1",
                ("singleParam", ("p1",), {}),
            ),
            (
                "-multiParam,p1,p2,p3",
                ("multiParam", ("p1", "p2", "p3"), {}),
            ),
            (
                "-singleOptionalParam,p1,,p3",
                ("singleOptionalParam", ("p1", "", "p3"), {}),
            ),
            (
                "-multiOptionalParam,,,p3",
                ("multiOptionalParam", ("", "", "p3"), {}),
            ),
            (
                "-endComma1,",
                ("endComma1", ("",), {}),
            ),
            (
                "-endComma2,,p3,",
                ("endComma2", ("", "p3", ""), {}),
            ),
            (
                "-singleKwParam,k1=v1",
                ("singleKwParam", (), dict(k1="v1")),
            ),
            (
                "-multiKwParam,k1=v1,k2=v2,k3=v3",
                ("multiKwParam", (), dict(k1="v1", k2="v2", k3="v3")),
            ),
            (
                "-mixed,p1,,,p3,k1=v1,k2=v2,k3=v3",
                ("mixed", ("p1", "", "", "p3"), dict(k1="v1", k2="v2", k3="v3")),
            ),
        )

        @pytest.mark.parametrize("string,expected", parameters)
        def test_name(self, string: str, expected: Any):
            opArg = OperatorToken(string)
            assert opArg._name == expected[0]

        @pytest.mark.parametrize("string,expected", parameters)
        def test_params(self, string: str, expected: Any):
            opArg = OperatorToken(string)
            assert opArg._params == list(expected[1])

        @pytest.mark.parametrize("string,expected", parameters)
        def test_kwparams(self, string: str, expected: Any):
            opArg = OperatorToken(string)
            assert opArg._kwparams == expected[2]


@pytest.mark.parametrize(
    "input,expected",
    [
        ["/some/path/out.nc", True],
        ["some/path/out.nc", True],
        ["so-me/path/out.nc", True],
        ["-some/path/out.nc", False],
        ["some path out.nc", True],
        ['"-some path out.nc"', True],
        ["'-some path out.nc'", True],
        ["'-some/path/out.nc'", True],
    ],
)
def test_FilePathToken(input: str, expected: bool):
    assert FilePathToken.is_match(input) == expected
