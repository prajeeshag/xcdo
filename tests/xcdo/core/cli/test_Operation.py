# type: ignore
import pytest
from pytest_mock import MockerFixture
from xcdo.core.cli.argument.tokens import OperatorToken
from xcdo.core.cli.operation import Operation
from xcdo.core.cli.registry import OperatorRegistry


@pytest.fixture
def token(mocker: MockerFixture):
    return mocker.Mock(spec=OperatorToken)


@pytest.fixture
def registry(mocker: MockerFixture):
    return mocker.Mock(spec=OperatorRegistry)


def test_called_registery_get(token, registry):
    token.name = "operator"

    Operation(token, registry)

    registry.get.assert_called_once_with("operator")


def test_operator_not_available(token, registry):
    token.name = "operator"
    registry.get.return_value = None

    Operation(token, registry)

    registry.get.assert_called_once_with("operator")
