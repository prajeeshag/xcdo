# type: ignore

import xarray as xr

from xcdo.io_utils import (
    _guess_engine,
    _guess_output_format,
    open_dataset,
    save_dataset,
)


def test_guess_engine_grib():
    assert _guess_engine("file.grib") == "cfgrib"
    assert _guess_engine("file.grb2") == "cfgrib"


def test_guess_engine_zarr():
    assert _guess_engine("data.zarr") == "zarr"
    assert _guess_engine("archive.zip") == "zarr"


def test_guess_engine_none():
    assert _guess_engine("data.nc") is None
    assert _guess_engine("file.txt") is None


def test_guess_output_format():
    assert _guess_output_format("a.zarr") == "zarr"
    assert _guess_output_format("a.zip") == "zarr"
    assert _guess_output_format("a.nc") == "netcdf"


def test_guess_output_grid_error():
    assert _guess_output_format("a.grib") == "netcdf"


def test_open_dataset_calls_xarray_open(mocker):
    mock_ds = xr.Dataset()
    mock_open = mocker.patch("xcdo.io_utils.xr.open_dataset", return_value=mock_ds)

    result = open_dataset("test.grib")

    mock_open.assert_called_once_with("test.grib", chunks={}, engine="cfgrib")
    assert result is mock_ds


def test_open_dataset_no_engine(mocker):
    mock_ds = xr.Dataset()
    mock_open = mocker.patch("xcdo.io_utils.xr.open_dataset", return_value=mock_ds)

    result = open_dataset("test.nc")

    mock_open.assert_called_once_with("test.nc", chunks={}, engine=None)
    assert result is mock_ds


def test_save_dataset_zarr(mocker):
    mock_to_zarr = mocker.patch("xcdo.io_utils.write_to_zarr")
    mock_to_nc = mocker.patch("xarray.Dataset.to_netcdf")

    ds = xr.Dataset()

    save_dataset(ds, "out.zarr")

    mock_to_zarr.assert_called_once_with(ds, "out.zarr")
    mock_to_nc.assert_not_called()


def test_save_dataset_netcdf(mocker):
    mock_to_zarr = mocker.patch("xarray.Dataset.to_zarr")
    mock_to_nc = mocker.patch("xarray.Dataset.to_netcdf")

    ds = xr.Dataset()

    save_dataset(ds, "out.nc")

    mock_to_nc.assert_called_once_with("out.nc")
    mock_to_zarr.assert_not_called()
