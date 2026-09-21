import pytest
from pydantic import ValidationError
from fly_in.model.map import Map
from fly_in.model.hub import Hub
from fly_in.model.connection import Connection


def test_map_creates_with_valid_data() -> None:
    hubs = {"start": Hub(name="start"), "goal": Hub(name="goal")}
    connections = [Connection(from_hub="start", to_hub="goal")]

    m = Map(
        nb_drones=2,
        hubs=hubs,
        connections=connections,
        start_hub="start",
        end_hub="goal",
    )
    assert m.nb_drones == 2
    assert "start" in m.hubs
    assert len(m.connections) == 1


def test_map_requires_nb_drones() -> None:
    with pytest.raises(ValidationError):
        Map.model_validate(
            {
                "hubs": {},
                "connections": [],
                "start_hub": "a",
                "end_hub": "b",
            }
        )
