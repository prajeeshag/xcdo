import typing as t

import xarray as xr
from clios import Input

from .validators import input_file_validator, open_dataset

DataSetInput = t.Annotated[
    xr.Dataset,
    Input(
        core_validation_phase="execute",
        build_phase_validators=(input_file_validator,),
        execute_phase_validators=(open_dataset,),
    ),
]

# DataSetOutput = t.Annotated[xr.Dataset, Output(callback=), xarray_to_dataset]
