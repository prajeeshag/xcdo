import enum
import typing as t

from typing_extensions import Doc

from xcdo import DatasetIn, DatasetOut, FloatParam, OperatorFns, Param

fn_registry = OperatorFns()


class SetMissExpr(enum.StrEnum):
    eq = "eq"
    gt = "gt"
    lt = "lt"
    ge = "ge"
    le = "le"


SetMissExprType = t.Annotated[
    SetMissExpr,
    Param(),
    Doc("Expression to set missing values, one of: eq, gt, lt, ge, le"),
]


@fn_registry.register()
def settomiss(
    input: DatasetIn,
    value: t.Annotated[FloatParam, Doc("")],
    expr: SetMissExprType = SetMissExpr.eq,
) -> DatasetOut:
    """
    Set values in a dataset to missing values.

    description:
        Set values in a dataset to missing values based on the given expression.
        default expression is `eq` (equal to), which means that values equal to the given value will be set to missing.
        other expressions are `gt` (greater than), `lt` (less than), `ge` (greater than or equal to), and `le` (less than or equal to).

    operator examples:
        xcdo -settomiss,0 infile.nc outfile.nc
        xcdo -settomiss,5,gt infile.nc outfile.nc
    """
    match expr:
        case SetMissExpr.eq:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] != value)
        case SetMissExpr.gt:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] <= value)
        case SetMissExpr.lt:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] >= value)
        case SetMissExpr.ge:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] < value)
        case SetMissExpr.le:
            for var in input.data_vars:
                input[var] = input[var].where(input[var] > value)
    return input
