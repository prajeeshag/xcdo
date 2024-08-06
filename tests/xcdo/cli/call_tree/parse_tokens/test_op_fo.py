# type: ignore

from dataclasses import dataclass

import pytest
from xcdo.cli.argument import FilePathToken as Ft
from xcdo.cli.argument import OperatorToken as Ot
from xcdo.cli.exceptions import ArgSyntaxError
from xcdo.cli.operation import GeneratorOperation as GOptn
from xcdo.cli.operation import WriteOperation as WOptn
from xcdo.cli.operator import Generator as Op
from xcdo.cli.operator import Writer as Wtr


@dataclass
class Input:
    tkns: list[Ot]
    op: Op
    wtr: Wtr

    @property
    def expected(self):
        optn = GOptn(
            self.op,
            args=self.tkns[0].params,
            kwargs=self.tkns[0].kwparams,
        )
        return WOptn(self.wtr, optn, (self.tkns[-1].path,))


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [Ot("op"), Ft("fout")],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
        Input(
            [
                Ot("op", ("1", "a"), (("b", "2"), ("c", "3"))),
                Ft("fout"),
            ],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
    ],
)
def test(mocker, calltree, input, token_parser, operators, writers, readers):
    operators.get.return_value = input.op
    writers.get.return_value = input.wtr

    res = calltree.parse_tokens(input.tkns)

    operators.get.assert_called_once_with(input.tkns[0].name)
    writers.get.assert_called_once_with(input.op.output_type)
    readers.get.assert_not_called()
    assert res == input.expected


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [Ot("op")],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
        Input(
            [
                Ot("op", ("1", "a"), (("b", "2"), ("c", "3"))),
            ],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
    ],
)
def test_missing_output(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    writers.get.return_value = input.wtr

    with pytest.raises(ArgSyntaxError) as e:
        calltree.parse_tokens(input.tkns)

    assert str(e.value) == "Missing output"
    assert e.value.token == str(input.tkns[0])


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [Ot("op"), Ft("fout"), Ot("op1")],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
        Input(
            [
                Ot("op", ("1", "a"), (("b", "2"), ("c", "3"))),
                Ft("fout"),
                Ft("fout"),
            ],
            Op(None, output_type=int),
            Wtr(None, int, 1),
        ),
    ],
)
def test_too_many_inputs(mocker, calltree, input, operators, writers, readers):
    operators.get.return_value = input.op
    writers.get.return_value = input.wtr

    with pytest.raises(ArgSyntaxError) as e:
        calltree.parse_tokens(input.tkns)

    assert str(e.value) == "Too many inputs"
    assert e.value.token == str(input.tkns[0])
