import typing as t

import rich

from xcdo import DatasetIn, DatasetOut, Doc, XcdoError
from xcdo import xarray as xr

from . import operator


@operator(name="print")
def print_dataset(input: DatasetIn) -> None:
    """
    Simply print the given dataset.

    description:
        This operator simply prints the given dataset to the terminal.
        It uses `rich` library to display the dataset in a more readable format.

    operator examples:
        xcdo -print infile.nc
        xcdo -print -selvar,var infile.nc
    """
    rich.print(input)


@operator(implicit="param")
def merge(
    *inputs: DatasetIn,
    compat: t.Literal[
        "identical", "equals", "broadcast_equals", "no_conflicts", "override", "minimal"
    ] = "no_conflicts",
    join: t.Literal["outer", "inner", "left", "right", "exact", "override"] = "outer",
    combine_attrs: t.Literal[
        "drop", "identical", "no_conflicts", "override"
    ] = "override",
) -> DatasetOut:
    """
    Merge multiple datasets into one.

    description:
        Use xarray's `merge` method to merge multiple datasets into one.
        Refer to xarray's documentation for more information regarding the options:
        https://docs.xarray.dev/en/stable/generated/xarray.merge.html

    operator examples:
        xcdo -merge infile1.nc infile2.nc infile2.nc outfile.nc
    """
    return xr.merge(inputs, compat=compat, join=join, combine_attrs=combine_attrs)


@operator()
def setchunk(
    inputs: DatasetIn,
    **chunks: t.Annotated[
        int, Doc("Chunk size for each dimension, e.g. -setchunk,time=10,lon=20")
    ],
) -> DatasetOut:
    """
    Set the chunk size of a dataset.

    description:
        Use xarray's `chunk` method to set the chunk size of a dataset.
        Refer to xarray's documentation for more information:
        https://docs.xarray.dev/en/stable/generated/xarray.Dataset.chunk.html

    operator examples:
        xcdo -setchunk,time=10 infile.nc outfile.nc
        xcdo -setchunk,time=10,lon=20,lat=10 infile.nc outfile.nc
    """
    try:
        return inputs.chunk(chunks)
    except ValueError as e:
        raise XcdoError(str(e))
