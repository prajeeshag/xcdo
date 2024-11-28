from xcdo import DatasetIn, OperatorFns
from xcdo.utils import get_xarray_from_dataset

fn_registry = OperatorFns()


@fn_registry.register()
def plot(input: DatasetIn) -> None:
    """
    A simple plot function for xarray DataArray.

    description:
        This function uses xarray.DataArray's `plot` method to plot the given dataset.
        It opens a interactive matplotlib window.

    operator examples:
        xcdo -plot infile.nc
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        raise ImportError("`matplotlib` is required for plotting")
    darray = get_xarray_from_dataset(input)
    darray.plot()  # type: ignore
    plt.show()
