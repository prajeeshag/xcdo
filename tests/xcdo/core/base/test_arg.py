from typing import Any

import pytest
from xcdo.core.cli.exceptions import ArgError
from xcdo.core.cli.operator_argument import OperatorArgument


def test_is_instance_of_arg():
    value = "   -simple   "
    arg = OperatorArgument(value)
    assert isinstance(arg, OperatorArgument)


def test_arg_strips_leading_spaces():
    value = "   -simple"
    arg = OperatorArgument(value)
    assert str(arg) == "-simple"


def test_arg_strips_trailing_spaces():
    value = "-simple   "
    arg = OperatorArgument(value)
    assert str(arg) == "-simple"


def test_arg_strips_leading_and_trailing_spaces():
    value = "   -simple   "
    arg = OperatorArgument(value)
    assert str(arg) == "-simple"


class Test_invalid:
    parameters: Any = (
        ("-simple,k1=v1=v2", (8, "Invalid parameter")),
        ("-simple,k1=v1,k1=v2", (14, "Parameter 'k1' is already assigned")),
        ("-simple,k2=v1,k1=v2,k2=v2", (20, "Parameter 'k2' is already assigned")),
    )

    @pytest.mark.parametrize("string,expected", parameters)
    def test_name(self, string: str, expected: Any):
        with pytest.raises(ArgError) as result:
            OperatorArgument(string)

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
        opArg = OperatorArgument(string)
        assert opArg.name == expected[0]

    @pytest.mark.parametrize("string,expected", parameters)
    def test_params(self, string: str, expected: Any):
        opArg = OperatorArgument(string)
        assert opArg.params == list(expected[1])

    @pytest.mark.parametrize("string,expected", parameters)
    def test_kwparams(self, string: str, expected: Any):
        opArg = OperatorArgument(string)
        assert opArg.kwparams == expected[2]
