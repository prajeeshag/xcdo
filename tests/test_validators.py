import pytest
import xarray as xr

from xcdo.exceptions import XcdoError
from xcdo.validators import (
    input_file_validator,
    output_file_validator,
    path_to_dataset_validator,
)


def test_input_file_validator_ok(tmp_path):
    f = tmp_path / "data.nc"
    f.write_text("dummy")
    assert input_file_validator(str(f)) == str(f)


def test_input_file_validator_missing(tmp_path):
    missing = tmp_path / "nope.nc"
    with pytest.raises(XcdoError) as err:
        input_file_validator(str(missing))
    assert "does not exist" in str(err.value)


def test_output_file_validator_ok(tmp_path):
    out = tmp_path / "result.nc"
    assert output_file_validator(str(out)) == str(out)


def test_output_file_validator_missing_dir(tmp_path):
    missing_dir = tmp_path / "abc" / "out.nc"
    with pytest.raises(XcdoError) as err:
        output_file_validator(str(missing_dir))
    assert "does not exist" in str(err.value)


def test_path_to_dataset_validator_dataset_passthrough():
    ds = xr.Dataset({"a": ("x", [1, 2, 3])})
    assert path_to_dataset_validator(ds) is ds


def test_path_to_dataset_validator_open_called(mocker):
    mock_ds = xr.Dataset()
    mock_open = mocker.patch("xcdo.validators.open_dataset", return_value=mock_ds)

    result = path_to_dataset_validator("dummy.nc")

    mock_open.assert_called_once_with("dummy.nc")
    assert result is mock_ds
