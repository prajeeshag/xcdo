# type: ignore
import pytest
from xcdo.core.cli.operator.operator import Operator

from .fn_samples import Input, fp1_param


class Test:
    @pytest.mark.parametrize(
        "input",
        [fp1_param],
    )
    def test_no_input(
        self,
        input: Input,
    ):
        op = Operator(input.fn)
        assert op.num_inputs == input.num_inputs
        for n in range(op.num_inputs):
            assert op.get_input_type(n) == input.input_types[n]
        assert op.num_args == input.num_args
        for n in range(op.num_args):
            assert op.get_arg_type(n) == input.arg_types[n]
