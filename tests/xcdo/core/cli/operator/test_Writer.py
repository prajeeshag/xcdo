from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Writer

from .testdata.writer import failing, passing


@pytest.mark.parametrize("input", failing)
def test_failing(input: Any):
    with pytest.raises(InvalidFunction) as e:
        Writer(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


@pytest.mark.parametrize("input", passing)
def test_passing(input: Any):
    reader = Writer(input.fn)
    assert reader.data_type == input.data_type
