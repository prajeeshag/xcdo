# type: ignore
import re

import pytest
import xarray as xr

from xcdo import XcdoError
from xcdo.operators.misc import setchunk


def test_setchunk_single_dim():
    ds = xr.Dataset({"a": (("time", "x"), [[1, 2], [3, 4]])})
    out = setchunk(inputs=ds, time=1)

    assert out.chunks["time"] == (1, 1)
    assert out.chunks["x"] == (2,)


def test_setchunk_multiple_dims():
    ds = xr.Dataset({"a": (("time", "lat", "lon"), [[[1, 2], [3, 4]]])})
    out = setchunk(inputs=ds, time=1, lat=1, lon=2)

    assert out.chunks["time"] == (1,)
    assert out.chunks["lat"] == (1, 1)
    assert out.chunks["lon"] == (2,)


def test_setchunk_invalid_dim():
    ds = xr.Dataset({"a": (("time", "x"), [[1, 2], [3, 4]])})

    with pytest.raises(
        XcdoError,
        match=re.escape(
            "chunks keys ('wrongdim',) not found in data dimensions ('time', 'x')"
        ),
    ):
        setchunk(inputs=ds, wrongdim=10)
