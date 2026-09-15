import pytest
from fly_in.parser.map_parser import MapParser


def test_parse_full_map(map_file):
    parser = MapParser(filepath=map_file)
    result = parser.parse()

    assert result.nb_drones == 4
    assert set(result.hubs.keys()) == {"start", "bottleneck", "wide_area", "goal"}
    assert result.start_hub == "start"
    assert result.end_hub == "goal"
    assert len(result.connections) == 3
    assert result.hubs["start"].color == "green"
    assert result.hubs["bottleneck"].color == "orange"
    assert result.hubs["bottleneck"].max_drones == 2
    assert result.hubs["wide_area"].color == "blue"
    assert result.hubs["wide_area"].max_drones == 3
    assert result.hubs["goal"].color == "red"

def test_parse_ignores_comments_and_blank_lines(map_file):
    parser = MapParser(filepath=map_file)
    result = parser.parse()
    assert result is not None


def test_parse_raises_on_unknown_directive(tmp_path):
    bad_path = tmp_path / "bad.map"
    bad_path.write_text("mystery_field: something\n")
    parser = MapParser(filepath=str(bad_path))

    with pytest.raises(ValueError, match="Unknown map directive"):
        parser.parse()
