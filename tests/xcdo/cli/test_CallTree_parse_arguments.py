# type: ignore

import pytest
from pytest_mock import MockerFixture
from xcdo.cli.argument import FilePathToken, OperatorToken
from xcdo.cli.call_tree import CallTree
from xcdo.cli.exceptions import OperatorNotFound, SyntaxError


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


@pytest.mark.parametrize(
    "input",
    [
        ["-operator"],
        ["-op1", "-op2", "f1", "f2"],
    ],
)
def test_call_tokenize(mocker, calltree, input, token_parser):
    calltree.parse_arguments(input)
    call = mocker.call
    token_parser.tokenize.assert_has_calls([call(x) for x in input], any_order=False)


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
        calltree.parse_arguments(len(input) * ["-op"])

    assert e.value.index == expected.index


@pytest.mark.parametrize(
    "input,expected",
    [
        [[OperatorToken("op1")], ["op1"]],
        [[OperatorToken("op1"), OperatorToken("op2")], ["op1", "op2"]],
        [[OperatorToken("op1"), FilePathToken("f2")], ["op1"]],
    ],
)
def test_call_operators_get(mocker, calltree, input, expected, token_parser, operators):
    token_parser.tokenize.side_effect = input
    calltree.parse_arguments(len(input) * ["-op"])
    call = mocker.call
    operators.get.assert_has_calls([call(x) for x in expected])


@pytest.mark.parametrize(
    "has_key, input, expected",
    [
        [
            [None, None, KeyError()],
            [OperatorToken(f"op{x}") for x in range(3)],
            OperatorNotFound("op2", 2),
        ],
        [
            [None, None, KeyError()],
            [FilePathToken("f1"), *tuple(OperatorToken(f"op{x}") for x in range(3))],
            OperatorNotFound("op2", 3),
        ],
    ],
)
def test_operator_not_found(
    mocker, calltree, input, has_key, expected, token_parser, operators
):
    token_parser.tokenize.side_effect = input
    operators.get.side_effect = has_key
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_arguments(len(input) * ["-op"])
    assert e.value.operator == expected.operator
    assert e.value.index == expected.index


@pytest.mark.parametrize(
    "input,expected",
    [
        [[FilePathToken("f1")], OperatorNotFound("f1", 0)],
        [[FilePathToken("f2"), OperatorToken("op2")], OperatorNotFound("f2", 0)],
    ],
)
def test_first_argument_not_operator(
    mocker, calltree, input, expected, token_parser, operators
):
    token_parser.tokenize.side_effect = input
    with pytest.raises(OperatorNotFound) as e:
        calltree.parse_arguments(len(input) * ["-op"])
    assert e.value.operator == expected.operator
    assert e.value.index == expected.index
