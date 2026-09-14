import pytest
from fly_in.parser.map_parser import MapParser


def test_parse_full_map(map_file):
    parser = MapParser(filepath=map_file)
    result = parser.parse()

    assert result.nb_drones == 2
    assert set(result.hubs.keys()) == {"start", "waypoint1", "waypoint2", "goal"}
    assert result.start_hub == "start"
    assert result.end_hub == "goal"
    assert len(result.connections) == 3
    assert result.hubs["start"].max_drones == 5
    assert result.hubs["waypoint1"].color == "blue"


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
