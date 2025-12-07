# type: ignore

from unittest.mock import patch

import numpy as np
import xarray as xr

from xcdo.io_utils import write_to_zarr


def test_write_to_zarr_performs_packing(tmp_path):
    ds = xr.Dataset(
        {
            "var": xr.DataArray(
                np.array([10.0, 20.0], dtype="float32"),
                dims=["x"],
            )
        }
    )

    # set encoding for packing
    ds["var"].encoding = {
        "dtype": "int16",
        "scale_factor": 0.5,
        "add_offset": 1.0,
    }

    out = tmp_path / "out.zarr"

    # patch actual zarr writing
    with patch.object(xr.Dataset, "to_zarr") as mock_zarr:
        write_to_zarr(ds, out)

    packed = ds["var"].values
    assert packed.dtype == np.int16
    assert np.array_equal(packed, np.array([18, 38], dtype=np.int16))

    mock_zarr.assert_called_once_with(out, mode="w", consolidated=False)


def test_write_to_zarr_skip_when_no_dtype(tmp_path):
    ds = xr.Dataset(
        {
            "var": xr.DataArray(
                np.array([10.0, 20.0], dtype="float32"),
                dims=["x"],
            )
        }
    )

    # set encoding for packing
    ds["var"].encoding = {
        "scale_factor": 0.5,
        "add_offset": 1.0,
    }

    out = tmp_path / "out.zarr"

    # patch actual zarr writing
    with patch.object(xr.Dataset, "to_zarr") as mock_zarr:
        write_to_zarr(ds, out)

    packed = ds["var"].values
    assert packed.dtype == np.float32
    assert np.array_equal(packed, np.array([10, 20], dtype=np.float32))

    mock_zarr.assert_called_once_with(out, mode="w", consolidated=False)


def test_write_to_zarr_skip_when_no_scale_or_offset(tmp_path):
    ds = xr.Dataset(
        {
            "var": xr.DataArray(
                np.array([10.0, 20.0], dtype="float32"),
                dims=["x"],
            )
        }
    )

    # set encoding for packing
    ds["var"].encoding = {
        "dtype": "float32",
    }

    out = tmp_path / "out.zarr"

    # patch actual zarr writing
    with patch.object(xr.Dataset, "to_zarr") as mock_zarr:
        write_to_zarr(ds, out)

    packed = ds["var"].values
    assert packed.dtype == np.float32
    assert np.array_equal(packed, np.array([10, 20], dtype=np.float32))

    mock_zarr.assert_called_once_with(out, mode="w", consolidated=False)


def test_write_to_zarr_multiple_vars(tmp_path):
    ds = xr.Dataset(
        {
            "var1": xr.DataArray(
                np.array([10.0, 20.0], dtype="float32"),
                dims=["x"],
            ),
            "var2": xr.DataArray(
                np.array([10.0, 20.0], dtype="float32"),
                dims=["x"],
            ),
        }
    )

    ds["var1"].encoding = {
        "dtype": "int16",
        "scale_factor": 0.5,
        "add_offset": 1.0,
    }
    ds["var2"].encoding = {
        "dtype": "int16",
        "scale_factor": 0.5,
        "add_offset": 1.0,
    }

    out = tmp_path / "out.zarr"

    # patch actual zarr writing
    with patch.object(xr.Dataset, "to_zarr") as mock_zarr:
        write_to_zarr(ds, out)

    packed = ds["var1"].values
    assert packed.dtype == np.int16
    assert np.array_equal(packed, np.array([18, 38], dtype=np.int16))

    packed = ds["var2"].values
    assert packed.dtype == np.int16
    assert np.array_equal(packed, np.array([18, 38], dtype=np.int16))
    mock_zarr.assert_called_once_with(out, mode="w", consolidated=False)
