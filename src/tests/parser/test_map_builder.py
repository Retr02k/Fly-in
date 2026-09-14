from fly_in.parser.map_builder import MapBuilder
from fly_in.model.hub import Hub


def test_map_builder_defaults():
    builder = MapBuilder()
    assert builder.nb_drones == 0
    assert builder.hubs == {}
    assert builder.connections == []
    assert builder.start_hub == ""
    assert builder.end_hub == ""


def test_map_builder_build_produces_valid_map():
    builder = MapBuilder()
    builder.nb_drones = 2
    builder.hubs = {"start": Hub(name="start"), "goal": Hub(name="goal")}
    builder.start_hub = "start"
    builder.end_hub = "goal"

    result = builder.build()
    assert result.nb_drones == 2
    assert result.start_hub == "start"
