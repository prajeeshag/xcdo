# type: ignore

import pytest
import xarray as xr
from cdo import Cdo

from xcdo import XcdoError
from xcdo.validators import input_file_validator, open_dataset, output_file_validator


@pytest.fixture
def cdo():
    return Cdo()


def test_input_file_validator_existing_file(tmp_path):
    file_path = tmp_path / "test_file.nc"
    file_path.touch()
    assert input_file_validator(str(file_path)) == str(file_path)


def test_input_file_validator_non_existing_file():
    with pytest.raises(XcdoError, match="File .* does not exist"):
        input_file_validator("non_existing_file.nc")


def test_input_file_validator_directory(tmp_path):
    dir_path = tmp_path / "test_dir"
    dir_path.mkdir()
    assert input_file_validator(str(dir_path)) == str(dir_path)


def test_output_file_validator_existing_parent(tmp_path):
    dir_path = tmp_path / "temp_file"
    assert output_file_validator(str(dir_path)) == str(dir_path)


def test_output_file_validator_non_existing_parent(tmp_path):
    dir_path = tmp_path / "some_non_existing_dir/temp_file"
    with pytest.raises(XcdoError, match="Directory .* does not exist"):
        output_file_validator(str(dir_path))


def test_open_dataset_nc(tmp_path, cdo):
    file_path = tmp_path / "test_file.nc"
    cdo.const("1,r18x9", output=str(file_path), options="-f nc")
    dataset = open_dataset(str(file_path))
    assert isinstance(dataset, xr.Dataset)
    assert dataset.sizes == {"lon": 18, "lat": 9}


@pytest.mark.parametrize("extension", ["grib", "grib1", "grb", "grb1"])
def test_open_dataset_grib1(tmp_path, cdo, extension):
    file_path = tmp_path / f"test_file.{extension}"
    cdo.const("1,r18x9", output=str(file_path), options="-f grb1")
    dataset = open_dataset(str(file_path))
    assert isinstance(dataset, xr.Dataset)
    assert dict(dataset.sizes) == {"longitude": 18, "latitude": 9}


@pytest.mark.parametrize("extension", ["grib2", "grb2"])
def test_open_dataset_grib2(tmp_path, cdo, extension):
    file_path = tmp_path / f"test_file.{extension}"
    cdo.const("1,r18x9", output=str(file_path), options="-f grb2")
    dataset = open_dataset(str(file_path))
    assert isinstance(dataset, xr.Dataset)
    assert dict(dataset.sizes) == {"longitude": 18, "latitude": 9}


@pytest.mark.parametrize("extension", ["zarr", "zip"])
def test_open_dataset_zarr(tmp_path, extension):
    file_path = tmp_path / f"test_file.{extension}"
    ds = xr.Dataset(
        {
            "temperature": xr.DataArray(
                data=[[1, 2], [3, 4]],
                dims=["latitude", "longitude"],
                coords={"latitude": [1, 2], "longitude": [1, 2]},
            )
        }
    )
    ds.to_zarr(str(file_path), mode="w")
    dataset = open_dataset(str(file_path))
    assert isinstance(dataset, xr.Dataset)
    assert dict(dataset.sizes) == {"longitude": 2, "latitude": 2}
