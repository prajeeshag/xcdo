import pytest
from xcdo.cli.registry import KeyExistsError, Registry


def test_set_get():
    reg = Registry[str, str]()
    reg.set("k", "object")
    assert reg.get("k") == "object"


def test_get_none():
    reg = Registry[str, str]()
    with pytest.raises(KeyError):
        reg.get("k")


def test_set_key_exist():
    reg = Registry[str, str]()
    reg.set("k", "object")
    with pytest.raises(KeyExistsError) as e:
        reg.set("k", "object")
    assert str(e.value) == "Key 'k' already exists. Reassignment is not allowed."
