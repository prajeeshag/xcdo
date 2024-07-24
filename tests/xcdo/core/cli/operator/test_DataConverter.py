from typing import Any

import pytest
from xcdo.core.cli.exceptions import DataConverterError
from xcdo.core.cli.operator import DataConverter

from .fn_samples import dcfailing, dcfailingruntime, dcpassing


@pytest.mark.parametrize("input", dcfailing)
def test_failing(input: Any):
    with pytest.raises(DataConverterError) as e:
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
    with pytest.raises(DataConverterError) as e:
        dc("s")
