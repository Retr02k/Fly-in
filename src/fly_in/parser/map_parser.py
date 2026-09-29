from typing import Callable
from pydantic import BaseModel
from fly_in.model.map import Map
from fly_in.parser.map_builder import MapBuilder
from fly_in.errors.custom_errors import MapParseError


HANDLERS: dict[str, Callable[[MapBuilder, str], None]] = {}


Handler = Callable[[MapBuilder, str], None]


def register(key: str) -> Callable[[Handler], Handler]:
    """Register a parser handler for a map directive.

    Args:
        key: Directive name appearing before the colon in a map line.

    Returns:
        A decorator that adds a handler to the global registry.
    """
    def decorator(fn: Handler) -> Handler:
        """Store and return a directive handler."""
        HANDLERS[key] = fn
        return fn

    return decorator


class MapParser(BaseModel):
    """Parse a map file into a validated map model."""
    filepath: str

    def parse(self) -> Map:
        """Read and validate the configured map file.

        Returns:
            The parsed and validated map.

        Raises:
            MapParseError: If a directive or structural rule is invalid.
            OSError: If the file cannot be opened.
        """
        from fly_in.parser import handlers  # noqa: F401

        builder = MapBuilder()

        with open(self.filepath) as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue
                builder.current_line = line_number

                key, _, value = line.partition(":")
                key, value = key.strip(), value.strip()

                handler = HANDLERS.get(key)
                if handler is None:
                    raise MapParseError(
                        self.filepath,
                        line_number,
                        f"unknown map directive {key!r}",
                    )
                try:
                    handler(builder, value)
                except MapParseError:
                    raise
                except (TypeError, ValueError) as error:
                    raise MapParseError(
                        self.filepath,
                        line_number,
                        str(error),
                    ) from error

        try:
            self._validate_builder(builder)
            return builder.build()
        except (TypeError, ValueError) as error:
            raise MapParseError(
                self.filepath,
                self._error_line(builder, str(error)),
                str(error),
            ) from error

    @staticmethod
    def _error_line(builder: MapBuilder, message: str) -> int:
        """Select the most relevant declaration line for a build error."""
        if "nb_drones" in message:
            return builder.nb_drones_line or 1
        if "start hub" in message:
            return builder.start_hub_line or 1
        if "end hub" in message:
            return builder.end_hub_line or 1
        return builder.current_line or 1

    @staticmethod
    def _validate_builder(builder: MapBuilder) -> None:
        """Validate parser-level required directives and connections."""
        if not builder.nb_drones_line:
            raise ValueError("missing nb_drones directive")
        if not builder.start_hub:
            raise ValueError("exactly one start_hub is required")
        if not builder.end_hub:
            raise ValueError("exactly one end_hub is required")
        hub_names = set(builder.hubs)
        seen_connections: set[frozenset[str]] = set()
        for connection, line in zip(
            builder.connections,
            builder.connection_lines,
            strict=True,
        ):
            if (
                connection.from_hub not in hub_names
                or connection.to_hub not in hub_names
            ):
                builder.current_line = line
                raise ValueError(
                    f"connection references unknown hub(s): "
                    f"{connection.from_hub!r}, {connection.to_hub!r}"
                )
            key = frozenset((connection.from_hub, connection.to_hub))
            if key in seen_connections:
                builder.current_line = line
                raise ValueError(
                    f"duplicate connection between "
                    f"{connection.from_hub!r} and {connection.to_hub!r}"
                )
            seen_connections.add(key)
