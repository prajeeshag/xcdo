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
def test_passing(input: Any, mocker: Any):
    writer = Writer(input.fn)
    assert writer.data_type == input.data_type
    assert writer.requires_file_path == input.requires_file_path


@pytest.mark.parametrize("n", [1, 2])
def test_callable(mocker: Any, n: int):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Writer.inspect_function")
    params = [("i", int, None), ("s", None, None)]
    args = ["i", "j"]
    inspect_function.return_value = (
        "name",
        params[0:n],
        None,
    )
    writer = Writer(fn)
    writer(*args[0:n])
    fn.assert_called_once_with(*args[0:n])
