import pytest
from pydantic import ValidationError
from fly_in.model.hub import Hub


def test_hub_creates_with_required_fields() -> None:
    hub = Hub(name="start")
    assert hub.name == "start"
    assert hub.x == 0
    assert hub.y == 0
    assert hub.max_drones == 1


def test_hub_rejects_empty_name() -> None:
    with pytest.raises(ValidationError):
        Hub(name="")


def test_hub_accepts_custom_coordinates_and_color() -> None:
    hub = Hub(name="waypoint1", x=2, y=3, color="blue")
    assert hub.x == 2
    assert hub.y == 3
    assert hub.color == "blue"


def test_hub_color_defaults_to_none() -> None:
    hub = Hub(name="waypoint1")
    assert hub.color is None
