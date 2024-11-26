import typing as t
from pathlib import Path

import xarray as xr
from clios import Input


def input_file_validator(path: str) -> str:
    assert Path(path).exists(), f"File {path} does not exist"
    assert Path(path).is_file(), f"Path {path} is not a file"
    return path


def open_dataset(path: str) -> xr.Dataset:
    return xr.open_dataset(path, engine="netcdf4", chunks={})  # pyright: ignore


DataSetInput = t.Annotated[
    xr.Dataset,
    Input(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
    ),
]
