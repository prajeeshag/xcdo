from xcdo import DatasetIn, OperatorFns

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
    darray = input.get_dataarray()
    darray.plot()  # type: ignore
    plt.show()
