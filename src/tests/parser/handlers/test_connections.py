from fly_in.parser.map_builder import MapBuilder
from fly_in.parser.handlers.connections import handle_connection


def test_handle_connection_parses_from_and_to() -> None:
    builder = MapBuilder()
    handle_connection(builder, "start-waypoint1")
    assert builder.connections[0].from_hub == "start"
    assert builder.connections[0].to_hub == "waypoint1"


def test_handle_connection_appends_multiple() -> None:
    builder = MapBuilder()
    handle_connection(builder, "a-b")
    handle_connection(builder, "b-c")
    assert len(builder.connections) == 2


def test_handle_connection_parses_max_link_capacity() -> None:
    builder = MapBuilder()
    handle_connection(builder, "a-b [max_link_capacity=2]")
    assert builder.connections[0].max_link_capacity == 2
