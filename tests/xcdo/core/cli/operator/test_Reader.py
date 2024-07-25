from typing import Any

import pytest
from xcdo.core.cli.exceptions import InvalidFunction
from xcdo.core.cli.operator import Reader

from .testdata.reader_testdata import failing, passing


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
    assert reader.output_type == input.out_type


def frf00(i: str) -> int:
    return "s"  # type: ignore


def frp00(i: str) -> int:
    return int(i)  # type: ignore


def test_rterror():
    reader = Reader(frf00)
    with pytest.raises(TypeError) as e:
        reader("s")
    assert str(e.value) == "Promised <int> but recieved <str> from function <frf00>"


def test_rtsuccess():
    reader = Reader(frp00)
    assert reader("1") == 1
