# type: ignore

import pytest
from pytest_mock import MockerFixture
from xcdo.core.cli.operation import Operation


@pytest.mark.parametrize(
    "args,kwargs,res",
    [
        [(), (), "s"],
        [("a", "1", "c"), (), 1],
        [("a", "1", "c"), (("k", "s"), ("l", "1")), 10.5],
    ],
)
def test_Operation(mocker: MockerFixture, args, kwargs, res):
    operator = mocker.patch(
        "xcdo.core.cli.operator.Operator", autospec=True
    ).return_value
    operator.load_args.return_value = args
    operator.load_kwargs.return_value = dict(kwargs)
    operator.return_value = res

    child_op1 = mocker.Mock()
    child_op2 = mocker.Mock()
    child_op1.execute.return_value = "op1"
    child_op2.execute.return_value = "op2"

    op = Operation(operator, args=args, kwargs=kwargs, children=(child_op1, child_op2))
    result = op.execute()
    operator.load_args.assert_called_once_with(args)
    operator.load_kwargs.assert_called_once_with(dict(kwargs))
    child_op1.execute.assert_called_once()
    child_op2.execute.assert_called_once()
    operator.assert_called_once_with(("op1", "op2"), *args, **dict(kwargs))
    assert result == res
