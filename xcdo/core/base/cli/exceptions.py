class ArgError(Exception):
    def __init__(self, pos: int, string: str, *args: object) -> None:
        self.pos = pos
        self.string = string
        super().__init__(*args)
