import pytest
import runpy
from pathlib import Path
from fly_in.parser.map_parser import MapParser


def test_parse_full_map(
    path_to_map_file: str,
    path_to_expected_output_file: str,
) -> None:
    expected = runpy.run_path(path_to_expected_output_file)["EXPECTED_MAP"]
    parser = MapParser(filepath=path_to_map_file)
    result = parser.parse()

    assert result.nb_drones == expected["nb_drones"]
    assert result.start_hub == expected["start_hub"]
    assert result.end_hub == expected["end_hub"]
    assert set(result.hubs) == set(expected["hubs"])
    assert len(result.connections) == len(expected["connections"])

    for hub_name, expected_hub in expected["hubs"].items():
        assert result.hubs[hub_name].model_dump() == expected_hub

    for connection, expected_connection in zip(
        result.connections,
        expected["connections"],
        strict=True,
    ):
        assert connection.model_dump() == expected_connection


def test_parse_ignores_comments_and_blank_lines(
    path_to_map_file: str,
) -> None:
    parser = MapParser(filepath=path_to_map_file)
    result = parser.parse()
    assert result is not None


def test_parse_raises_on_unknown_directive(tmp_path: Path) -> None:
    bad_path = tmp_path / "bad.map"
    bad_path.write_text("mystery_field: something\n")
    parser = MapParser(filepath=str(bad_path))

    with pytest.raises(ValueError, match="Unknown map directive"):
        parser.parse()
