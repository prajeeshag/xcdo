#
import numpy as np
import pytest
import xarray as xr

from xcdo import XcdoError
from xcdo.operators.misc import float2short


def test_float2short_basic():
    ds = xr.Dataset({"a": ("x", np.array([1.0, 2.0, 3.0], dtype=np.float32))})
    data_range = 3.0 - 1.0
    info = np.iinfo(np.int16)
    max_range = info.max - info.min
    scale_factor = data_range / max_range
    add_offset = 1.0 - scale_factor * info.min
    out = float2short(ds)
    encoding = out["a"].encoding

    assert out["a"].dtype == np.float32
    assert encoding["dtype"] == np.int16
    np.testing.assert_allclose(
        encoding["scale_factor"], scale_factor, rtol=1e-6, atol=1e-12
    )
    np.testing.assert_allclose(
        encoding["add_offset"], add_offset, rtol=1e-6, atol=1e-12
    )
    assert out["a"].encoding["_FillValue"] == -32767


def test_float2short_range_too_large():
    ds = xr.Dataset({"a": ("x", np.array([0.0, 1e9], dtype=np.float64))})

    with pytest.raises(XcdoError, match="too large for int16"):
        float2short(ds)


def test_float2short_removes_attrs():
    ds = xr.Dataset({"a": ("x", [1.0, 2.0])})
    ds["a"].attrs["_FillValue"] = -9999
    ds["a"].attrs["missing_value"] = -9999

    out = float2short(ds)

    assert "_FillValue" not in out["a"].attrs
    assert "missing_value" not in out["a"].attrs
