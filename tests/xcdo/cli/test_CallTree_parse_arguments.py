# type: ignore

import pytest
from pytest_mock import MockerFixture
from xcdo.cli.call_tree import CallTree


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


def test_call_tokenize(calltree, token_parser, argv, res):
    calltree.parse_arguments()
