# type: ignore

import pytest
from xcdo.cli.exceptions import InvalidFunction
from xcdo.cli.operator import Reader, reader_factory

from .testdata.reader_invalid_fns import failing


@pytest.mark.parametrize("input", failing)
def test_failing(input):
    with pytest.raises(InvalidFunction) as e:
        reader_factory(input.fn)
    assert str(e.value) == str(input.e)
    assert e.value.fn == input.e.fn
    assert e.value.pname == input.e.pname


def fp02(input: str) -> int: ...


def test_passing():
    op = reader_factory(fp02)
    assert op == Reader(fp02, int)
