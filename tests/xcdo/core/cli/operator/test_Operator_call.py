# type: ignore
import inspect

import pytest
from xcdo.core.cli.operator import Operator

_nil = inspect.Parameter.empty


@pytest.mark.parametrize(
    "args,kwds,res",
    [
        [["s"], {"k": 1}, 1],
        [[], {"k": 1}, "s"],
        [["s"], {}, True],
        [["s", "i"], {}, 10.5],
        [[], {"k": 1, "f": "s"}, None],
    ],
)
def test_call(mocker, args, kwds, res):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Operator.inspect_function")
    params = [("i", int, None)]
    inspect_function.return_value = ("name", params[:], type(res))
    operator = Operator(fn)
    fn.return_value = res
    result = operator(*args, **kwds)
    fn.assert_called_once_with(*args, **kwds)
    assert result == res


def test_typeerror(mocker):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Operator.inspect_function")
    params = [("i", int, None)]
    inspect_function.return_value = ("name", params[:], int)
    operator = Operator(fn)
    fn.return_value = "s"
    with pytest.raises(TypeError) as e:
        operator()
    assert str(e.value) == "Expected <int> but received <str> from function <name>"
