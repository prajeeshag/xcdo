# type: ignore

from dataclasses import dataclass

import pytest
from xcdo.cli.argument import FilePathToken as Ft
from xcdo.cli.argument import OperatorToken as Ot
from xcdo.cli.exceptions import ArgSyntaxError
from xcdo.cli.operation import Operation as Optn
from xcdo.cli.operation import ReadOperation as ROptn
from xcdo.cli.operation import WriteOperation as WOptn
from xcdo.cli.operator import Operator as Op
from xcdo.cli.operator import Reader as Rdr
from xcdo.cli.operator import Writer as Wtr
from xcdo.cli.operator._Operator import _Input as I


@dataclass
class Input:
    tkns: list[Ot]
    op: Op
    wtr: Wtr
    rdr: Rdr

    @property
    def expected(self):
        roptns = [
            ROptn(self.rdr, self.tkns[i + 1].path) for i in range(len(self.tkns) - 2)
        ]
        optn = Optn(
            self.op,
            tuple(roptns),
            args=self.tkns[0].params,
            kwargs=self.tkns[0].kwparams,
        )
        return WOptn(self.wtr, optn, (self.tkns[-1].path,))


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [Ot("op"), Ft("fi1"), Ft("fi2"), Ft("fi3"), Ft("fo")],
            Op(None, output_type=int, input=I((int, str, float))),
            Wtr(None, int, 1),
            Rdr(None, int),
        ),
    ],
)
def test(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    readers.get.return_value = input.rdr
    writers.get.return_value = input.wtr

    res = calltree.parse_tokens(input.tkns)

    call = mocker.call
    operators.get.assert_called_once_with(input.tkns[0].name)
    writers.get.assert_called_once_with(input.op.output_type)
    readers.get.assert_has_calls(
        [call(input.op.input.dtypes[i]) for i in range(input.op.input.len)],
        any_order=False,
    )
    assert res == input.expected


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [
                Ot("op", ("a",), (("b", "1"),)),
                Ft("fi1"),
                Ft("fi2"),
                Ft("fi3"),
                Ft("fo"),
            ],
            Op(None, output_type=int, input=I((int, str))),
            Wtr(None, int, 1),
            Rdr(None, int),
        ),
    ],
)
def test_too_many_inputs(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    readers.get.return_value = input.rdr
    writers.get.return_value = input.wtr

    with pytest.raises(ArgSyntaxError) as e:
        calltree.parse_tokens(input.tkns)

    assert str(e.value) == "Too many inputs"
    assert e.value.token == "-op,a,b=1"


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [
                Ot("op", ("a",), (("b", "1"),)),
                Ft("fi1"),
                Ft("fo"),
            ],
            Op(None, output_type=int, input=I((int, str))),
            Wtr(None, int, 1),
            Rdr(None, int),
        ),
    ],
)
def test_missing_input(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    readers.get.return_value = input.rdr
    writers.get.return_value = input.wtr

    with pytest.raises(ArgSyntaxError) as e:
        calltree.parse_tokens(input.tkns)

    assert str(e.value) == "Missing inputs"
    assert e.value.token == str(input.tkns[0])


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [
                Ot("op", ("a",), (("b", "1"),)),
            ],
            Op(None, output_type=int, input=I((int, str))),
            Wtr(None, int, 1),
            Rdr(None, int),
        ),
    ],
)
def test_missing_output(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    readers.get.return_value = input.rdr
    writers.get.return_value = input.wtr

    with pytest.raises(ArgSyntaxError) as e:
        calltree.parse_tokens(input.tkns)

    assert str(e.value) == "Missing output"
    assert e.value.token == str(input.tkns[0])
