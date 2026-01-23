import pytest
import xarray as xr

import xcdo.xarray_accessors  # noqa: F401
from xcdo import XcdoError


def test_single_var_returns_dataarray():
    ds = xr.Dataset({"temp": ("x", [1, 2, 3])})
    da = ds.get_dataarray()
    assert isinstance(da, xr.DataArray)
    assert da.name == "temp"
    assert da.values.tolist() == [1, 2, 3]


def test_multiple_vars_raises():
    ds = xr.Dataset(
        {
            "temp": ("x", [1, 2]),
            "precip": ("x", [3, 4]),
        }
    )
    with pytest.raises(XcdoError, match="Dataset should have a single data variable"):
        ds.get_dataarray()


def test_zero_vars_raises():
    ds = xr.Dataset()
    with pytest.raises(XcdoError, match="No data variables found"):
        ds.get_dataarray()
