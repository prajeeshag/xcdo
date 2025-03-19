import cf_xarray as cf_xarray
import xarray as xarray


@xarray.register_dataset_accessor("get_dataarray")  # type: ignore
class GetDataArray:
    def __init__(self, dataset: xarray.Dataset):
        self._dataset = dataset

    def __call__(self) -> xarray.DataArray:
        """
        Get a DataArray from a Dataset

        if the Dataset has only one data variable, return that variable as a DataArray

        Raises:
            AssertionError: if the Dataset has multiple data variables
        """
        assert (
            len(self._dataset.data_vars) == 1
        ), f"Dataset should have a single data variable, Got {self._dataset.data_vars}"
        return self._dataset.to_array()


custom_criteria = {
    "time": {
        "name": "Time|time|times|Times",
    }
}
cf_xarray.set_options(custom_criteria=custom_criteria)  # type: ignore
