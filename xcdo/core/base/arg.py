class Arg(str):
    def __new__(cls, value: str) -> "Arg":
        value = value.strip()
        return super().__new__(cls, value)
