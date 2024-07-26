from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Converter

from .testdata.converter import (
    dcfailing,
    dcfailingruntime,
    dcpassing,
)


@pytest.mark.parametrize("input", dcfailing)
def test_failing(input: Any):
    with pytest.raises(InvalidFunction) as e:
        Converter(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


@pytest.mark.parametrize("input", dcpassing)
def test_passing(input: Any):
    dc = Converter(input.fn)
    assert dc.input_type == input.input_type
    assert dc.output_type == input.output_type


def test_callable(mocker: Any):
    fn = mocker.Mock()
    inspect_function = mocker.patch(
        "xcdo.core.cli.operator._Converter.inspect_function"
    )
    params = [("i", str, None)]
    inspect_function.return_value = ("name", params[:], int)
    converter = Converter(fn)
    fn.return_value = 1
    result = converter("s")
    fn.assert_called_once_with("s")
    assert result == 1


@pytest.mark.parametrize("input", dcfailingruntime)
def test_runtimefail(input: Any):
    dc = Converter(input.fn)
    with pytest.raises(TypeError) as e:
        dc("s")
    assert str(e.value) == str(input.e)
