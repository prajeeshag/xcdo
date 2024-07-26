from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Reader

from .testdata.reader import failing, passing


@pytest.mark.parametrize("input", failing)
def test_failing(input: Any):
    with pytest.raises(InvalidFunction) as e:
        Reader(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


@pytest.mark.parametrize("input", passing)
def test_passing(input: Any):
    reader = Reader(input.fn)
    assert reader.data_type == input.out_type


def test_callable(mocker: Any):
    fn = mocker.Mock()
    inspect_function = mocker.patch("xcdo.core.cli.operator._Reader.inspect_function")
    params = [("i", None, None)]
    inspect_function.return_value = ("name", params[:], int)
    reader = Reader(fn)
    fn.return_value = 1
    result = reader("s")
    fn.assert_called_once_with("s")
    assert result == 1


def frf00(i: str) -> int:
    return "s"  # type: ignore


def test_rterror():
    reader = Reader(frf00)
    with pytest.raises(TypeError) as e:
        reader("s")
    assert str(e.value) == "Promised <int> but recieved <str> from function <frf00>"
