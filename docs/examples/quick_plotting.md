# Example: quick plotting

Use the [`-plot`](../operators/plot.md) operator to quickly plot a dataset, like so:

```bash
$ xcdo -plot infile.nc
```
!!! warning
    This is give an error if the dataset has multiple data variables.
    Use the [`-selvar`](../operators/selvar.md) operator to select a single data variable


### Dataset with multiple data variables

If the dataset has multiple data variables, use the [`-selvar`](../operators/selvar.md) operator to select a single data variable, like so:

```bash
$ xcdo -plot -selvar,var1 infile.nc
```

### Plotting a single time step
```bash
$ xcdo -plot -isel,time=0 -selvar,var1 infile.nc
```

!!! Note
    The [`-plot`](../operators/plot.md) operator interally use xarray's `plot` method, which plots line plots for 1D data, pcolormesh plots for 2D data, and histograms for 3D and above data.


### Plotting the fldmean using CDO fldmean operator

```bash
$ xcdo -plot -cdo -fldmean -selvar,var1 infile.nc
```
!!! warning "cdo should be installed"
    The [`-cdo`](../operators/cdo.md) operator requires the CDO executable to be installed and available in your PATH.

You can basically chain any number of operators together and give it to the [`-plot`](../operators/plot.md) operator and it will plot the result, for example:
```bash
$ xcdo -plot -isel,lon=50 -selvar,var1 infile.nc
$ xcdo -plot -cdo -fldmean -ymonmean -selvar,var1 infile.nc
```

### Saving the plot to a file
```bash
$ xcdo -plot,figure.png -cdo -fldmean -selvar,var1 infile.nc
```
