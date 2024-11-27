import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, IntParam, OperatorFns, StrParam

fn_registry = OperatorFns()


@fn_registry.register(name="selname")
@fn_registry.register()
def selvar(
    DatasetIn: DatasetIn, name: t.Annotated[StrParam, Doc("Name of the variable")]
) -> DatasetOut:
    """
    Select a data variable from a dataset.

    operator examples:
        xcdo -selvar,tas infile.nc outfile.nc
    """
    try:
        return DatasetIn.data_vars[name].to_dataset()
    except KeyError:
        raise ValueError(
            f"`{name}` is not data variable! Available {DatasetIn.data_vars}"
        )


@fn_registry.register(name="isel")
def isel(
    DatasetIn: DatasetIn, **indexes: t.Annotated[IntParam, Doc("Indexes to select")]
) -> DatasetOut:
    """
    Use xarray's isel method to select data from a dataset.

    operator examples:
        xcdo -isel,time=0,lon=100 infile.nc outfile.nc
    """
    return DatasetIn.isel(
        indexes,
    )
