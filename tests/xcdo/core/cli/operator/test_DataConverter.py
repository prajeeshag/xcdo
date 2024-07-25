from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import DataConverter

from .testdata.data_converter import (
    dcfailing,
    dcfailingruntime,
    dcpassing,
    dcpassingruntime,
)


@pytest.mark.parametrize("input", dcfailing)
def test_failing(input: Any):
    with pytest.raises(InvalidFunction) as e:
        DataConverter(input.fn)
    assert str(e.value) == input.msg


@pytest.mark.parametrize("input", dcpassing)
def test_passing(input: Any):
    dc = DataConverter(input.fn)
    assert dc.input_type == input.input_type
    assert dc.output_type == input.output_type


@pytest.mark.parametrize("input", dcfailingruntime)
def test_runtimefail(input: Any):
    dc = DataConverter(input.fn)
    with pytest.raises(RuntimeError) as e:
        dc("s")
    assert str(e.value) == input.msg


@pytest.mark.parametrize("input", dcpassingruntime)
def test_runtimesuccess(input: Any):
    dc = DataConverter(input[0])
    assert isinstance(dc(10.5), input[1])
