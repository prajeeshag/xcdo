import xarray as xr


def _guess_engine(path: str) -> str | None:
    grib_extensions = [".grib", ".grib1", ".grb", ".grb1", ".grib2", ".grb2"]
    zarr_extensions = [".zarr", ".zip"]
    for ext in grib_extensions:
        if path.endswith(ext):
            return "cfgrib"
    for ext in zarr_extensions:
        if path.endswith(ext):
            return "zarr"
    return None


def _guess_output_format(path: str) -> str:
    """Guess the output format based on the file extension"""
    if path.endswith(".zarr") or path.endswith(".zip"):
        return "zarr"
    return "netcdf"


def open_dataset(path: str) -> xr.Dataset:
    engine = _guess_engine(path)
    return xr.open_dataset(  # pyright: ignore
        path,
        chunks={},
        engine=engine,
    )


def write_to_zarr(dataset: xr.Dataset, path: str) -> None:
    for name, da in dataset.data_vars.items():
        enc = da.encoding

        # packing only if dtype and at least one of scale/add_offset exist
        target_dtype = enc.get("dtype")
        if target_dtype is None:
            continue

        scale = enc.get("scale_factor")
        offset = enc.get("add_offset")

        if scale is None and offset is None:
            continue

        # default scale/offset if only one is provided
        scale = 1.0 if scale is None else scale
        offset = 0.0 if offset is None else offset

        packed = ((da.data - offset) / scale).astype(target_dtype)

        dataset[name] = xr.DataArray(
            packed,
            coords=da.coords,
            dims=da.dims,
            attrs=da.attrs,
        )
        dataset[name].encoding = da.encoding
    dataset.to_zarr(path, mode="w", consolidated=False)


def save_dataset(dataset: xr.Dataset, path: str) -> None:
    format = _guess_output_format(path)
    if format == "zarr":
        write_to_zarr(dataset, path)
        # dataset.to_zarr(path, mode="w")  # pyright: ignore
        return
    dataset.to_netcdf(path)  # pyright: ignore
