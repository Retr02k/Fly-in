import pytest

from fly_in.model.drone import Drone, DroneStatus


def test_drone_starts_at_the_beginning_of_its_route():
    drone = Drone(
        drone_id=1,
        current_hub="start",
        route=["start", "goal"],
    )

    assert drone.current_route_index == 0
    assert drone.status == DroneStatus.WAITING


def test_drone_requires_a_positive_id():
    with pytest.raises(ValueError):
        Drone(
            drone_id=0,
            current_hub="start",
            route=["start", "goal"],
        )
