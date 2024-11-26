import typing as t
from pathlib import Path

import xarray as xr
from pydantic import BeforeValidator


def input_file_validator(path: str) -> str:
    assert Path(path).exists(), f"File {path} does not exist"
    return path


def output_file_validator(path: str) -> str:
    parent = Path(path).parent
    assert parent.exists(), f"Directory {parent} does not exist"
    return path


def _xarray_to_dataset(input: t.Any) -> t.Any:
    if isinstance(input, xr.DataArray):
        return input.to_dataset()
    return input


xarray_to_dataset = BeforeValidator(_xarray_to_dataset)


def _guess_engine(path: str) -> str | None:
    grib_extensions = [".grib", ".grib1", ".grb", ".grb1", ".grib2", ".grb2"]
    zarr_extensions = [".zarr", ".zip"]
    for ext in grib_extensions:
        if path.endswith(ext):
            return "cfgrib"
    for ext in zarr_extensions:
        if path.endswith(ext):
            return "zarr"
    return None


def open_dataset(path: str) -> xr.Dataset:
    engine = _guess_engine(path)
    return xr.open_dataset(  # pyright: ignore
        path,
        chunks={},
        engine=engine,
    )
