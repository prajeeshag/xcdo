# type: ignore
import inspect
from typing import Annotated

import pytest
from xcdo.core.cli.exceptions import InvalidArguments as Error
from xcdo.core.cli.operator import Operator

from .testdata.operator_valid_fns import _toBoolReader

_nil = inspect.Parameter.empty


@pytest.mark.parametrize(
    "params,args,kwds,res",
    [
        [
            [("*i", int, _nil)],
            [10, 20],
            dict(j=1),
            Error("Got an unexpected keyword argument [j]"),
        ],
        [
            [("*i", int, _nil), ("j", int, _nil)],
            [10, 20],
            dict(),
            Error("Missing required keyword argument [j]"),
        ],
        [[], [10, 20], dict(), Error("Expected 0 argument(s), got 2")],
        [[("i", int, _nil)], [], dict(), Error("Expected 1 argument(s), got 0")],
        [[("i", int, _nil)], [10, 20], dict(), Error("Expected 1 argument(s), got 2")],
    ],
)
def test_wrong_inputs(mocker, params, args, kwds, res):
    op = arrange(mocker, params)
    with pytest.raises(Error) as e:
        op.load_params(args, kwds)
    assert str(e.value) == str(res)


@pytest.mark.parametrize(
    "params,args,kwds,res",
    [
        [[("*i", int, _nil)], ["1", "2"], dict(), ((1, 2), {})],
        [[("i", int, _nil), ("j", float, _nil)], ["1", "2"], dict(), ((1, 2.0), {})],
        [[("*i", int, _nil), ("j", float, _nil)], [], dict(j="2"), ((), {"j": 2.0})],
        [[("**i", int, _nil)], [], dict(j="2"), ((), {"j": 2})],
        [
            [("*j", str, _nil), ("**i", int, _nil)],
            ["abcd", "1234"],
            dict(j="2"),
            (("abcd", "1234"), {"j": 2}),
        ],
        [[("input", int, _nil), ("**i", int, _nil)], [], dict(j="2"), ((), {"j": 2})],
        [
            [("*i", Annotated[bool, _toBoolReader], _nil)],
            ["1", "0"],
            dict(),
            ((True, False), {}),
        ],
    ],
)
def test_valid_inputs(mocker, params, args, kwds, res):
    op = arrange(mocker, params)
    result = op.load_params(args, kwds)
    assert result == res


def arrange(mocker, params):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Operator.inspect_function")
    inspect_function.return_value = ("name", params, None)
    op = Operator(fn)
    return op
