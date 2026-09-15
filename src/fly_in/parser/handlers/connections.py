from fly_in.model.connection import Connection
from fly_in.parser.map_builder import MapBuilder
from fly_in.parser.map_parser import register
import re


@register("connection")
def handle_connection(builder: MapBuilder, value: str) -> None:
    match = re.fullmatch(
        r"(?P<from_hub>\S+)-(?P<to_hub>\S+)"
        r"(?:\s+\[max_link_capacity=(?P<capacity>\d+)\])?",
        value.strip(),
    )

    if match is None:
        raise ValueError(f"Invalid connection syntax: {value!r}")

    capacity_text = match.group("capacity")
    capacity = int(capacity_text) if capacity_text is not None else 1

    builder.connections.append(
        Connection(
            from_hub=match.group("from_hub"),
            to_hub=match.group("to_hub"),
            max_link_capacity=capacity,
        )
    )
