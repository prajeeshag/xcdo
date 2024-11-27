import typing as t

import xarray as xr
from clios import Input, Output, Param

from .utils import save_dataset
from .validators import input_file_validator, path_to_dataset_validator

DatasetIn = t.Annotated[
    xr.Dataset,
    Input(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
        execute_phase_validators=(path_to_dataset_validator,),
    ),
]

DatasetParam = t.Annotated[
    xr.Dataset,
    Param(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
        execute_phase_validators=(path_to_dataset_validator,),
    ),
]

DatasetOut = t.Annotated[xr.Dataset, Output(callback=save_dataset, strict=False)]
