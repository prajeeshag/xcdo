class CdoError(Exception):
    def __init__(
        self, msg: str = "", stdout: str = "", stderr: str = "", returncode: int = 1
    ):
        super().__init__(msg)
        self.msg: str = msg
        self.stdout: str = stdout
        self.stderr: str = stderr
        self.returncode: int = returncode

    def __str__(self) -> str:
        res = ""
        res += f"{self.stdout}\n\n" if self.stdout else ""
        res += f"{self.stderr}\n\n" if self.stderr else ""
        res += f"---\n{self.msg}" if self.msg else ""
        return res


class CacheError(Exception):
    pass
