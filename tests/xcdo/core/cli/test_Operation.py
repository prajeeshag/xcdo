# type: ignore
# import pytest
# from pytest_mock import MockerFixture
# from xcdo.core.cli.argument.tokens import OperatorToken
# from xcdo.core.cli.operator import Operator
# from xcdo.core.cli.operation import Operation
# from xcdo.core.cli.exceptions import OperatorNotFound
#
#
# @pytest.fixture
# def token(mocker: MockerFixture):
#    return mocker.Mock(spec=OperatorToken)
#
#
# @pytest.fixture
# def operator(mocker: MockerFixture):
#    return mocker.Mock(spec=Operator)
#
#
# def test_called_registery_get(token, operator):
#    Operation(token, operator)
#    registry.get.assert_called_once_with("operator")
#
#
# def test_operator_not_available(token, registry):
#    token.name = "operator"
#    registry.get.return_value = None
#
#    with pytest.raise(OperatorNotFound) as e:
#        Operation(token, registry)

