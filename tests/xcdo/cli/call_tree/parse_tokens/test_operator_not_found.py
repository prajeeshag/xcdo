# type: ignore
import pytest
from xcdo.cli.argument import OperatorToken as Ot
from xcdo.cli.exceptions import OperatorNotFound


@pytest.mark.parametrize(
    "input, expected",
    [
        [
            [Ot("op1")],
            OperatorNotFound("op1"),
        ],
    ],
)
def test_operator_not_found(mocker, calltree, input, expected, operators):
    operators.get.side_effect = KeyError()
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_tokens(input)
    assert e.value.operator == expected.operator
