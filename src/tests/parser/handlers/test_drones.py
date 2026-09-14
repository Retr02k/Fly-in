from fly_in.parser.map_builder import MapBuilder
from fly_in.parser.handlers.drones import handle_nb_drones


def test_handle_nb_drones_converts_to_int():
    builder = MapBuilder()
    handle_nb_drones(builder, "2")
    assert builder.nb_drones == 2
    assert isinstance(builder.nb_drones, int)
