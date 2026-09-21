from fly_in.parser.map_builder import MapBuilder
from fly_in.parser.handlers.hubs import (
    _parse_hub_fields,
    handle_end_hub,
    handle_hub,
    handle_start_hub,
)


def test_parse_hub_fields_with_all_settings() -> None:
    hub = _parse_hub_fields("start 0 0 [zone=normal color=green max_drones=5]")
    assert hub.name == "start"
    assert hub.x == 0
    assert hub.y == 0
    assert hub.color == "green"
    assert hub.max_drones == 5


def test_parse_hub_fields_with_partial_settings() -> None:
    hub = _parse_hub_fields("waypoint1 1 0 [color=blue]")
    assert hub.color == "blue"
    assert hub.max_drones == 1


def test_parse_hub_fields_with_no_brackets() -> None:
    hub = _parse_hub_fields("waypoint2 2 0")
    assert hub.color is None


def test_parse_hub_fields_with_negative_coordinates() -> None:
    hub = _parse_hub_fields("origin -1 -2 [color=red]")
    assert hub.x == -1
    assert hub.y == -2


def test_handle_start_hub_sets_builder_state() -> None:
    builder = MapBuilder()
    handle_start_hub(builder, "start 0 0 [color=green]")
    assert builder.start_hub == "start"
    assert "start" in builder.hubs


def test_handle_end_hub_sets_builder_state() -> None:
    builder = MapBuilder()
    handle_end_hub(builder, "goal 3 0 [color=red]")
    assert builder.end_hub == "goal"


def test_handle_hub_does_not_set_start_or_end() -> None:
    builder = MapBuilder()
    handle_hub(builder, "waypoint1 1 0 [color=blue]")
    assert "waypoint1" in builder.hubs
    assert builder.start_hub == ""
    assert builder.end_hub == ""
