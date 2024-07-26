# type: ignore
from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Operator

from .testdata.operator import Input, failing, passing


@pytest.mark.parametrize("input", failing)
def test_failing(input):
    with pytest.raises(InvalidFunction) as e:
        Operator(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


@pytest.mark.parametrize("input", passing)
def test_passing(input: Input):
    op = Operator(input.fn)
    assert op.num_inputs == input.num_inputs
    assert op.is_variadic_input == input.variadic_input
    if op.is_variadic_input:
        assert op.get_input_type() == input.input_types[0]
    for n in range(op.num_inputs):
        assert op.get_input_type(n) == input.input_types[n]
    assert op.num_args == input.num_args
    for n in range(op.num_args):
        assert op.get_arg_name(n) == input.args[n][0]
        assert op.get_arg_type(n) == input.args[n][1]
    assert op.var_arg == input.var_arg[0]
    assert op.var_arg_type == input.var_arg[1]
    assert op.kwarg_keys == tuple(input.kwargs.keys())
    for k in op.kwarg_keys:
        assert op.get_kwarg_type(k) == input.kwargs[k][0]
        assert op.get_kwarg_default_value(k) == input.kwargs[k][1]
    assert op.var_kwarg == input.var_kwarg[0]
    assert op.var_kwarg_type == input.var_kwarg[1]
    assert op.output_type == input.output_type


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
def test_callable(mocker: Any, args: Any, kwds: Any, res: Any):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Operator.inspect_function")
    params = [("i", int, None)]
    inspect_function.return_value = ("name", params[:], type(res))
    operator = Operator(fn)
    fn.return_value = res
    result = operator(*args, **kwds)
    fn.assert_called_once_with(*args, **kwds)
    assert result == res


def test_typeerror(mocker: Any):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Operator.inspect_function")
    params = [("i", int, None)]
    inspect_function.return_value = ("name", params[:], int)
    operator = Operator(fn)
    fn.return_value = "s"
    with pytest.raises(TypeError) as e:
        operator()
    assert str(e.value) == "Expected <int> but received <str> from function <name>"
