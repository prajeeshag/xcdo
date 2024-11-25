import typing as t

import xarray as xr
from clios import Input

DataSetInput = t.Annotated[xr.Dataset, Input(core_validation_phase="execute")]
