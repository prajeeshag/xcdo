import pytest
from xcdo.core.cli.argument_token import ArgumentToken


def test_argument_token():
    with pytest.raises(TypeError) as e:

        class TestArgument(ArgumentToken):  # type: ignore
            pass

    assert str(e.value) == "TestArgument class must have attribute 'pattern'"
