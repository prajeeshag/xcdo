# type: ignore
import pytest
from xcdo.core.cli.exceptions import OperatorDefError
from xcdo.core.cli.operator.operator import Operator

from .fn_samples import Input, failing, passing


@pytest.mark.parametrize("input", passing)
def test_passing(input: Input):
    op = Operator(input.fn)
    assert op.num_inputs == input.num_inputs
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


@pytest.mark.parametrize("input", failing)
def test_failing(input):
    with pytest.raises(OperatorDefError) as e:
        Operator(input.fn)
    assert str(e.value) == input.msg
