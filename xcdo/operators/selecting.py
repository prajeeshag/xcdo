import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, IntParam, OperatorFns, StrParam

fn_registry = OperatorFns()


@fn_registry.register(name="selname")
@fn_registry.register()
def selvar(
    input: DatasetIn,
    name: t.Annotated[StrParam, Doc("Name of the variable")],
) -> DatasetOut:
    """
    Select a data variable from a dataset.

    operator examples:
        xcdo -selvar,tas infile.nc outfile.nc
        xcdo -selname,tas infile.nc outfile.nc
    """
    try:
        return input.data_vars[name].to_dataset()
    except KeyError:
        raise ValueError(f"`{name}` is not data variable! Available {input.data_vars}")


@fn_registry.register(name="isel")
def isel(
    DatasetIn: DatasetIn, **indexes: t.Annotated[IntParam, Doc("Indexes to select")]
) -> DatasetOut:
    """
    Index along specified dimensions.

    description:
        Use xarray's `isel` method to return a new dataset with each array indexed along the specified dimension(s).

    operator examples:
        xcdo -isel,time=0,lon=100 infile.nc outfile.nc
    """
    return DatasetIn.isel(
        indexes,
    )
