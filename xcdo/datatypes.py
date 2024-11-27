import typing as t

import xarray as xr
from clios import Input, Output, Param

from .validators import input_file_validator, open_dataset, save_dataset

DatasetIn = t.Annotated[
    xr.Dataset,
    Input(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
        execute_phase_validators=(open_dataset,),
    ),
]

DatasetParam = t.Annotated[
    xr.Dataset,
    Param(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
        execute_phase_validators=(open_dataset,),
    ),
]

DatasetOut = t.Annotated[xr.Dataset, Output(callback=save_dataset)]
