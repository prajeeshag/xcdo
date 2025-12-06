<style>
</style>
# Writing Custom Operators

Any Python function can become an XCDO operator if:

- It uses the `@operator()` decorator.
- It follows some basic type-hint conventions.

## A simple example
This operator just prints the input dataset to the console.

```py title="dump.py"
# dump.py
from xcdo import operator, DatasetIn

@operator()
def dump(ds_in: DatasetIn) -> None:
    print(ds_in)
```

What this means:

- `@operator()` tells XCDO that function `dump` is an operator.
- `ds_in: DatasetIn` says the operator expects one dataset as input.
- `-> None` means it doesn’t return anything (it just prints).

Call this from the command line:

```bash
$ xcdo -dump.py input.nc
```

or if dump.py is in another directory, call it by its path like:

```bash
$ xcdo -/path/to/dump.py input.nc
```

### What XCDO does behind the scenes?

When you run those commands, XCDO:

1.	Loads the given Python file (e.g. dump.py).
2.	Finds the function decorated with @operator().
3.	Reads the type hints of that function:
    - Here it sees `ds_in: DatasetIn`
4.	Uses those type hints to:
    - Work out how many inputs the operator takes.
    - Understand their types (e.g. one DatasetIn).

### What is `DatasetIn`?

`ds_in: DatasetIn` simply tells XCDO that your operator expects an `xarray.Dataset` as the input and XCDO will take care of turning your command-line arguments into that dataset for you.


## Example: an operator with parameters and output

let's consider an operator `selvar.py` that takes one input dataset, one variable name as parameter, and returns a datasets as output.

```py title="selvar.py"
from xcdo import operator, DatasetIn, DatasetOut

@operator()
def selvar(ds_in: DatasetIn, name: str) -> DatasetOut:
    return ds_in[name].to_dataset() # (1)
```

1. The `.to_dataset()` is necessary because, `ds_in[name]` is a `xarray.DataArray` and `selvar` returns a `xarray.Dataset`

This can be called from the command line:

```bash
$ xcdo -selvar.py,sst input.nc out.nc
```

The selvar operator introduces two new ideas:

1. Parameters (`name: str`), just like the `ds_in: DatasetIn`, parameters are function arguments. On the command line, they appear as comma-separated values immediately after the operator name: `-selvar.py,sst`
- Return value (`-> DatasetOut`) - The operator returns a `xarray.Dataset`, so XCDO expects an output filename on the command line: `out.nc`

!!! Note
    As `selvar.py` returns a dataset, it can be an input to another operator. For example:
    ```bash
    $ xcdo -timemean -zonmean -selvar.py,sst input.nc out.nc
    $ xcdo -plot -selvar.py,sst input.nc
    # Or to our own custom operator
    $ xcdo -dump.py -selvar.py,sst input.nc
    ```

!!! Note
    We didn't explicitly write any code:

    - to load the input dataset from the command-line argument `input.nc`
    - to write the output dataset to `out.nc`.

    This is done by XCDO under the hood.


## Example: an operator with multiple inputs
```py title="example.py"
from xcdo import operator, DatasetIn, DatasetOut

@operator()
def example(ds1: DatasetIn, ds2: DatasetIn, ds3: DatasetIn) -> DatasetOut:
    # do something with ds1, ds2 and ds3
    return ds1 # return the result
```

```bash
$ xcdo -example.py infile1.nc infile2.nc outfile.nc
```

## Example: an operator with variable inputs

```py title="example.py"
from xcdo import operator, DatasetIn, DatasetOut

@operator()
def example(*ds_list: DatasetIn) -> DatasetOut:
    # do something with ds_list
    return ds_list[0] # return the result
```

```bash
$ xcdo -example.py infile1.nc infile2.nc outfile.nc
$ xcdo -example.py infile1.nc infile2.nc infile3.nc outfile.nc
$ xcdo -example.py infile1.nc infile2.nc infile3.nc infile4.nc outfile.nc
```

## More on parameters

Suppported parameter types are:
- `str`
- `int`
- `float`
- `date`
- `datetime`
- `time`
- `timedelta`
- `bool`
- `DatasetParam` -  which is an `xarray.Dataset` but now as a parameter

!!! Note
    For `date`, `datetime` and `timedelta`, XCDO expects strings in the [RFC3339](https://datatracker.ietf.org/doc/html/rfc3339) format, such as:
    Date: YYYY-MM-DD
    Time: HH:MM:SS
    DateTime: YYYY-MM-DDTHH:MM:SS
    Duration: PnYnMnDTnHnMnS
    and more.
    see the [speedate](https://docs.rs/speedate/latest/speedate/) documentation for more full details.


lets look at an example:

```py title="example.py"
from xcdo import operator, DatasetIn, DatasetOut, DatasetParam
from datetime import date, datetime, timedelta, time

@operator()
def example(
    ds_param: DatasetParam,
    name: str,
    step: int,
    val: float,
    flag: bool,
    date: date,
    time: time,
    dt: datetime,
    td: timedelta
) -> None:
    print(ds_param)
    print(name, step, val, flag, date, time, dt, td)
```

```bash
$ xcdo -example.py,file.nc,var,3,1.0,T,2022-01-01,12:00:00,2022-01-01T12:00:00,P1Y
```
