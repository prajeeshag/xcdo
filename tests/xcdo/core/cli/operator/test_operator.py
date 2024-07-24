# type: ignore
import pytest
from xcdo.core.cli.operator.operator import Operator

from .fn_samples import Input, passing


class Test:
    @pytest.mark.parametrize(
        "input",
        passing,
    )
    def test_passing(
        self,
        input: Input,
    ):
        op = Operator(
            input.fn,
        )
        assert op.num_inputs == input.num_inputs
        for n in range(op.num_inputs):
            assert op.get_input_type(n) == input.input_types[n]
        assert op.num_args == input.num_args
        for n in range(op.num_args):
            assert op.get_arg_type(n) == input.arg_types[n]
            assert op.get_arg_name(n) == input.arg_names[n]
        assert op.variadic_arg_present == input.variadic_arg_present
        assert op.variadic_arg_type == input.variadic_arg_type
        assert op.kwarg_keys == input.kwarg_keys
        for k in op.kwarg_keys:
            assert op.get_kwarg_type(k) == input.kwarg_types[k]
            assert op.get_kwarg_default_value(k) == input.kwarg_default_values[k]
        assert op.variadic_kwarg_present == input.variadic_kwarg_present
        assert op.variadic_kwarg_type == input.variadic_kwarg_type
        assert op.output_type == input.output_type
