import xarray as xr


def get_xarray_from_dataset(dataset: xr.Dataset) -> xr.DataArray:
    """
    Get a DataArray from a Dataset

    if the Dataset has only one data variable, return that variable as a DataArray

    Raises:
        AssertionError: if the Dataset has multiple data variables
    """
    assert len(dataset.data_vars) == 1, "Dataset should have a single data variable"
    return dataset.to_array()
