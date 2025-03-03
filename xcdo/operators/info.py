from xcdo import DatasetIn

from . import operator


@operator()
def showtimestamp(
    input: DatasetIn,
) -> None:
    """
    Show time stamp

    operator examples:
        xcdo -showtimestamp infile.nc
    """
    time_coord = input.cf.get("time", None)

    if time_coord is not None:
        print(time_coord.values)
    else:
        raise ValueError("No 'time' coordinate found in the dataset")
