# type: ignore
import pytest
from xcdo.cli.argument import FilePathToken as Ft
from xcdo.cli.argument import OperatorToken as Ot
from xcdo.cli.exceptions import OperatorNotFound


@pytest.mark.parametrize(
    "input,expected",
    [
        [[Ft("f2"), Ot("op2")], OperatorNotFound("f2")],
    ],
)
def test_first_argument_not_operator(mocker, calltree, input, expected):
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_tokens(input)
    assert e.value.operator == expected.operator
