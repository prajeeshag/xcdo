# type: ignore
from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Operator

from .testdata.operator_invalid_fns import failing
from .testdata.operator_valid_fns import passing


@pytest.mark.parametrize("input", failing)
def test_failing(input):
    with pytest.raises(InvalidFunction) as e:
        Operator(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


@pytest.mark.parametrize("input", passing)
def test_passing(input: Any):
    op = Operator(input.fn)
    assert op.num_inputs == input.num_inputs
    assert op.is_variadic_input == input.variadic_input
    if op.is_variadic_input:
        assert op.get_input_type() == input.input_types[0]
    for n in range(op.num_inputs):
        assert op.get_input_type(n) == input.input_types[n]

    assert op.num_args == input.num_args
    for n in range(op.num_args):
        arg = op.get_arg(n)
        assert arg.name == input.args[n].name
        assert arg.dtype == input.args[n].dtype
        assert arg.data_reader == input.args[n].data_reader

    assert bool(op.var_arg) == bool(input.var_arg)
    if op.var_arg:
        assert op.var_arg.dtype == input.var_arg.dtype
        assert op.var_arg.data_reader == input.var_arg.data_reader

    assert op.required_kwarg_keys == tuple(input.required_kwargs.keys())
    for k in op.required_kwarg_keys:
        arg = op.get_kwarg(k)
        assert arg.dtype == input.required_kwargs[k].dtype
        assert arg.data_reader == input.required_kwargs[k].data_reader
        assert arg.default == input.required_kwargs[k].default

    assert op.optional_kwarg_keys == tuple(input.kwargs.keys())
    for k in op.optional_kwarg_keys:
        arg = op.get_kwarg(k)
        assert arg.dtype == input.kwargs[k].dtype
        assert arg.data_reader == input.kwargs[k].data_reader
        assert arg.default == input.kwargs[k].default

    assert bool(op.var_kwarg) == bool(input.var_kwarg)
    if op.var_kwarg:
        assert op.var_kwarg.dtype == input.var_kwarg.dtype
        assert op.var_kwarg.data_reader == input.var_kwarg.data_reader

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
