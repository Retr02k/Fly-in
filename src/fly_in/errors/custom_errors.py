class MapParseError(ValueError):
    """Describe a map-format error with its source location."""

    def __init__(
        self,
        filepath: str,
        line: int,
        message: str,
    ) -> None:
        """Create an error for a specific map file and source line.

        Args:
            filepath: Path of the map being parsed.
            line: One-based physical line number where parsing failed.
            message: Human-readable explanation of the invalid input.
        """
        self.filepath = filepath
        self.line = line
        self.message = message
        super().__init__(f"{filepath}: line {line}: {message}")
