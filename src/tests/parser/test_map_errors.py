from pathlib import Path

import pytest

from fly_in.errors.custom_errors import MapParseError
from fly_in.parser.map_parser import MapParser


def test_invalid_connection_reports_file_and_line(tmp_path: Path) -> None:
    map_path = tmp_path / "invalid.map"
    map_path.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "end_hub: goal 1 0\n"
        "connection: start--goal\n"
    )

    with pytest.raises(MapParseError) as error:
        MapParser(filepath=str(map_path)).parse()

    assert f"{map_path}: line 4:" in str(error.value)
    assert "Invalid connection syntax" in str(error.value)


def test_invalid_drone_count_reports_file_and_line(tmp_path: Path) -> None:
    map_path = tmp_path / "invalid.map"
    map_path.write_text("nb_drones: many\n")

    with pytest.raises(MapParseError, match=r"line 1:") as error:
        MapParser(filepath=str(map_path)).parse()
    assert "nb_drones must be a valid integer" in str(error.value)


def test_zero_drone_count_reports_declaration_line(tmp_path: Path) -> None:
    map_path = tmp_path / "invalid.map"
    map_path.write_text("nb_drones: 0\n")

    with pytest.raises(MapParseError, match=r"line 1:") as error:
        MapParser(filepath=str(map_path)).parse()
    assert "nb_drones must be greater than zero" in str(error.value)


def test_duplicate_hub_reports_declaration_line(tmp_path: Path) -> None:
    map_path = tmp_path / "duplicate.map"
    map_path.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "hub: start 1 0\n"
        "end_hub: goal 2 0\n"
    )

    with pytest.raises(MapParseError, match=r"line 3: Duplicate hub name"):
        MapParser(filepath=str(map_path)).parse()


def test_multiple_start_hubs_are_rejected(tmp_path: Path) -> None:
    map_path = tmp_path / "multiple-start.map"
    map_path.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "start_hub: other 1 0\n"
        "end_hub: goal 2 0\n"
    )

    with pytest.raises(MapParseError, match=r"line 3:"):
        MapParser(filepath=str(map_path)).parse()


def test_duplicate_coordinates_are_rejected(tmp_path: Path) -> None:
    map_path = tmp_path / "coordinates.map"
    map_path.write_text(
        "nb_drones: 1\n"
        "start_hub: start 0 0\n"
        "hub: waypoint 0 0\n"
        "end_hub: goal 2 0\n"
    )

    with pytest.raises(MapParseError, match=r"same coordinates"):
        MapParser(filepath=str(map_path)).parse()


def test_missing_start_hub_is_rejected(tmp_path: Path) -> None:
    map_path = tmp_path / "missing-start.map"
    map_path.write_text(
        "nb_drones: 1\n"
        "hub: waypoint 0 0\n"
        "end_hub: goal 1 0\n"
    )

    with pytest.raises(MapParseError, match=r"exactly one start_hub"):
        MapParser(filepath=str(map_path)).parse()
