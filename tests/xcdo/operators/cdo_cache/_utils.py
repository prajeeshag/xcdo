from pathlib import Path
import random
import string


def randomword(
    n: int = 10,
    prefix: str = "",
    suffix: str = "",
):
    letters = string.ascii_lowercase
    return prefix + "".join(random.choice(letters) for _ in range(n)) + suffix


def randomcmd():
    return randomword(prefix="-")


def randomfile(tmp_path: Path) -> Path:
    return tmp_path / randomword()
