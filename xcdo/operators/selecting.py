import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, FloatParam, IntParam, StrParam

from . import operator


@operator(name="selname")
@operator()
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


@operator(name="isel")
def isel(
    input: DatasetIn, **indexes: t.Annotated[IntParam, Doc("Indexes to select")]
) -> DatasetOut:
    """
    Index along specified dimensions.

    description:
        Use xarray's `isel` method to return a new dataset with each array indexed along the specified dimension(s).

    operator examples:
        xcdo -isel,time=0,lon=100 infile.nc outfile.nc
    """
    return input.isel(
        indexes,
    )


@operator()
def sellonlatbox(
    input: DatasetIn,
    wlon: t.Annotated[FloatParam, Doc("Western longitude")],
    elon: t.Annotated[FloatParam, Doc("Eastern longitude")],
    slat: t.Annotated[FloatParam, Doc("Southern latitude")],
    nlat: t.Annotated[FloatParam, Doc("Northern latitude")],
) -> DatasetOut:
    """
    Select a region using the longitude and latitude bounds.

    description:
        Use xarray's `sel` method to select a region using the longitude and latitude bounds.

    operator examples:
        xcdo -sellonlatbox,-180,180,-90,90 infile.nc outfile.nc
    """
    lon_name, lat_name = input.lon.name, input.lat.name
    return input.sel(
        {lon_name: slice(wlon, elon), lat_name: slice(slat, nlat)},
    )
