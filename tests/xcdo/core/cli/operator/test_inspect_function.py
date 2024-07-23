# type: ignore

import pytest
from xcdo.core.cli.operator._utils import inspect_function

from .fn_samples import fn1_param, fn2_param


@pytest.mark.parametrize("input,expected", [fn1_param, fn2_param])
def test_passing(input, expected):
    assert inspect_function(input) == expected
