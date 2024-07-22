import pytest
from xcdo.core.cli.argument.token import ArgumentToken


def test_pattern():
    with pytest.raises(TypeError) as e:

        class TestArgument(ArgumentToken):  # type: ignore
            pass

    assert str(e.value) == "TestArgument class must have attribute 'pattern'"


def test_pattern_type():
    with pytest.raises(TypeError) as e:

        class TestArgument(ArgumentToken[str]):  # type: ignore
            pattern = 1  # type: ignore
            pass

    assert (
        str(e.value)
        == "TestArgument class attribute 'pattern' should be a <str> or re.Pattern object"
    )
