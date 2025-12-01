<style>
</style>
# XCDO

![Test](https://github.com/prajeeshag/xcdo/actions/workflows/test.yml/badge.svg)
![Doc](https://github.com/prajeeshag/xcdo/actions/workflows/build-docs.yml/badge.svg)
![PyPI - Version](https://img.shields.io/pypi/v/xcdo)
[![codecov](https://codecov.io/gh/prajeeshag/xcdo/graph/badge.svg?token=UNNUW30IQL)](https://codecov.io/gh/prajeeshag/xcdo)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


## What is XCDO?
Hey there! If you've ever worked with climate or NWP model data, you probably know about [CDO](https://code.mpimet.mpg.de/projects/cdo) (Climate Data Operators). It's a super useful tool—fast, efficient, and written in C/C++ (I guess 🤨). I built XCDO as a Python-based alternative that mimics CDO while making it easier to extend, script, and integrate seamlessly with the original CDO. Under the hood, XCDO is powered by another Python library called [Clios](https://github.com/prajeeshag/clios) (again created by me 🤓), and all the heavy lifting for data handling is done using [Xarray](https://docs.xarray.dev/en/stable/).

## Why XCDO?
One might ask so why another CDO like tool which is ofcourse will be slugish than the superfast CDO? And actually you are kind of right, it might not be very useful and infact this was just a fun project I came up with to learn serious software development using Python. However, there are some features which might make this tool relevant and those are:

- Written in python and uses existing capabilities of Xarray. Extending and writting new operators are much easier in python. Potential for open source community development.
- You can write a simple python function and use it as a custom operator of XCDO and can be used just like a operator which comes a long with XCDO. This enables you to write clean, organised and reusable analysis codes without leaving the intuitive CDO interface. Everything can be just an XCDO operator which can be mixed-matched to create any complex analysis.
- As it also integrates to the original CDO using the “-cdo” operator, you can make use of the efficient CDO operators whenever possible and integrate it to the XCDO operators or your custom operators seamlessly.
- CDO currently doesn’t support Zarr files, but since Xarray does, specifically for NetCDF data in Zarr format, XCDO—built on Xarray—naturally supports Zarr as well. In fact, this is where I primarily use XCDO, as it allows me to quickly check Zarr data from the command line, which is especially useful when working with a lot of Zarr files.

## Installation
<!--termynal-->
```
$ pip install xcdo
```

## Usage
To get a list of all available operators and their short descriptions, use:
<!--termynal--->
```
$ xcdo --list
```

To get detailed information about a specific operator, use:
<!--termynal--->
```
# xcdo --show <operator>
$ xcdo --show selvar
```

As it mimics the CDO interface, using XCDO is generally the same as using CDO. for e.g:
<!--termynal--->
```
$ xcdo -selvar,var1 indata.nc outdata.nc
$ xcdo -timemean -zonmean in.nc out.nc
```

For a more complete example including more features, see the Tutorial - User Guide.