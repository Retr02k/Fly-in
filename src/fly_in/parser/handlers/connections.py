from parser.map_parser import register
from parser.map_builder import MapBuilder
from model.connection import Connection


@register("connection")
def handle_connection(builder: MapBuilder, value: str) -> None:
    from_hub, _, to_hub = value.partition("-")
    builder.connections.append(Connection(from_hub=from_hub, to_hub=to_hub))
