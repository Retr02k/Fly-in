class MapParseError(ValueError):
    def __init__(
        self,
        filepath: str,
        line: int,
        message: str,
    ) -> None:
        self.filepath = filepath
        self.line = line
        self.message = message
        super().__init__(f"{filepath}: line {line}: {message}")
