import pytest
from xcdo.core.cli.argument_token import ArgumentToken


def test_pattern():
    with pytest.raises(TypeError) as e:

        class TestArgument(ArgumentToken):  # type: ignore
            pass

    assert str(e.value) == "TestArgument class must have attribute 'pattern'"


def test_pattern_type():
    with pytest.raises(TypeError) as e:

        class TestArgument(ArgumentToken):  # type: ignore
            pattern = 1
            pass

    assert (
        str(e.value)
        == "TestArgument class attribute 'pattern' should be a re.Pattern object"
    )
