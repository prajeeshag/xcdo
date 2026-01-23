#
import numpy as np
import pytest
import xarray as xr

from xcdo import DatasetIn
from xcdo.operators.renaming import rename, renamedim  # adjust import


@pytest.fixture
def sample_ds() -> DatasetIn:
    data = xr.DataArray(
        np.arange(4).reshape(2, 2),
        dims=("lat", "lon"),
        coords={"lat": [10, 20], "lon": [30, 40]},
        name="var",
    )
    return DatasetIn(data.to_dataset())


def _get_var(ds):
    return list(ds.data_vars.values())[0]


def test_renamedim(sample_ds):
    out = renamedim(sample_ds, "lat", "latitude")
    var = _get_var(out)

    assert "latitude" in var.dims
    assert "lat" not in var.dims
    assert var.shape == (2, 2)


def test_rename(sample_ds):
    out = rename(sample_ds, "var", "temperature")

    assert "temperature" in out.data_vars
    assert "var" not in out.data_vars

    new = out["temperature"]
    old = _get_var(sample_ds)

    np.testing.assert_array_equal(new.values, old.values)
