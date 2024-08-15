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


def randomfile(tmp_path: Path) -> str:
    return str(tmp_path / randomword())


def create_randomfile(tmp_path: Path) -> str:
    file_path = tmp_path / randomword()
    file_path.write_text(" ")
    return str(file_path)
