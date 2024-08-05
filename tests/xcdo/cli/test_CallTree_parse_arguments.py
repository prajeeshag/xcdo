# type: ignore

from dataclasses import dataclass, field

import pytest
from pytest_mock import MockerFixture
from xcdo.cli.argument import FilePathToken as FPtkn
from xcdo.cli.argument import OperatorToken as OpTkn
from xcdo.cli.call_tree import CallTree
from xcdo.cli.exceptions import OperatorNotFound, SyntaxError
from xcdo.cli.operation import GeneratorOperation as GOptn
from xcdo.cli.operation import Operation as Optn
from xcdo.cli.operation import ReadOperation as ROptn
from xcdo.cli.operation import WriteOperation as WOptn
from xcdo.cli.operator import Operator as Op
from xcdo.cli.operator import Reader as Rdr
from xcdo.cli.operator import Writer as Wtr
from xcdo.cli.operator._Operator import _Input as I


@pytest.fixture
def operators(mocker: MockerFixture):
    return mocker.patch(
        "xcdo.cli.registry.OperatorRegistry", autospec=True
    ).return_value


@pytest.fixture
def readers(mocker: MockerFixture):
    return mocker.patch("xcdo.cli.registry.ReaderRegistry", autospec=True).return_value


@pytest.fixture
def writers(mocker: MockerFixture):
    return mocker.patch("xcdo.cli.registry.WriterRegistry", autospec=True).return_value


@pytest.fixture
def token_parser(mocker: MockerFixture):
    return mocker.patch("xcdo.cli.argument.TokenParser", autospec=True).return_value


@pytest.fixture
def calltree(
    operators,
    readers,
    writers,
    token_parser,
):
    return CallTree(
        operators,
        writers,
        readers,
        token_parser,
    )


@dataclass
class Input:
    tkns: list[OpTkn]
    optkn: OpTkn
    op: Op
    wtr: Wtr
    rdr: Rdr
    fi: FPtkn
    fo: FPtkn

    def __post_init__(self):
        roptn = ROptn(self.rdr, self.fi)
        optn = Optn(
            self.op,
            (roptn,),
            args=self.optkn.params,
            kwargs=self.optkn.kwparams,
        )
        self.excepted = WOptn(self.wtr, optn, (self.fo,))


@pytest.mark.parametrize(
    "input",
    [
        Input(
            [OpTkn("op"), FPtkn("fin"), FPtkn("fout")],
            OpTkn("op"),
            Op(None, output_type=int, input=I((int,))),
            Wtr(None, int, 1),
            Rdr(None, int),
            "fin",
            "fout",
        ),
        # Input(
        #     [OpTkn("op"), FPtkn("fin1"), FPtkn("fin2"), FPtkn("fout")],
        #     OpTkn("op"),
        #     Op(None, output_type=int, input=I((int, str))),
        #     Wtr(None, int, 1),
        #     Rdr(None, int),
        #     "fin",
        #     "fout",
        # ),
        Input(
            [
                OpTkn("op", ("1", "a"), (("b", "2"), ("c", "3"))),
                FPtkn("fin"),
                FPtkn("fout"),
            ],
            OpTkn("op", ("1", "a"), (("b", "2"), ("c", "3"))),
            Op(None, output_type=int, input=I((int,))),
            Wtr(None, int, 1),
            Rdr(None, int),
            "fin",
            "fout",
        ),
    ],
)
def test_valid(mocker, calltree, input, token_parser, operators, writers, readers):
    operators.get.return_value = input.op
    readers.get.return_value = input.rdr
    writers.get.return_value = input.wtr

    res = calltree.parse_tokens(input.tkns)

    call = mocker.call
    operators.get.assert_called_once_with(input.optkn.name)
    writers.get.assert_called_once_with(input.op.output_type)
    readers.get.assert_has_calls(
        [call(input.op.input.dtypes[i]) for i in range(input.op.input.len)],
        any_order=False,
    )
    assert res == input.excepted


@pytest.mark.parametrize(
    "input,expected",
    [
        [
            [None, None, SyntaxError(pos=5, msg="Error1")],
            SyntaxError(index=2, pos=5, msg="Error1"),
        ],
        [
            [None, SyntaxError(pos=5, msg="Error1")],
            SyntaxError(index=1, pos=5, msg="Error1"),
        ],
    ],
)
def test_SyntaxError(mocker, calltree, input, expected, token_parser):
    token_parser.tokenize.side_effect = input
    with pytest.raises(SyntaxError) as e:
        calltree.tokenize(len(input) * ["-op"])

    assert e.value.index == expected.index


@pytest.mark.parametrize(
    "input, expected",
    [
        [
            [OpTkn("op1")],
            OperatorNotFound("op1", 0),
        ],
    ],
)
def test_operator_not_found(mocker, calltree, input, expected, operators):
    operators.get.side_effect = KeyError()
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_tokens(input)
    assert e.value.operator == expected.operator
    assert e.value.index == expected.index


@pytest.mark.parametrize(
    "input,expected",
    [
        [[FPtkn("f2"), OpTkn("op2")], OperatorNotFound("f2", 0)],
    ],
)
def test_first_argument_not_operator(mocker, calltree, input, expected):
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_tokens(input)
    assert e.value.operator == expected.operator
    assert e.value.index == expected.index
