import pytest

from fly_in.model.drone import Drone, DroneStatus
from fly_in.model.transit import TransitState


def test_drone_starts_at_the_beginning_of_its_route() -> None:
    drone = Drone(
        drone_id=1,
        current_hub="start",
        route=["start", "goal"],
    )

    assert drone.current_route_index == 0
    assert drone.status == DroneStatus.WAITING


def test_drone_requires_a_positive_id() -> None:
    with pytest.raises(ValueError):
        Drone(
            drone_id=0,
            current_hub="start",
            route=["start", "goal"],
        )


def test_drone_can_record_active_transit() -> None:
    transit = TransitState(
        origin_hub="start",
        destination_hub="restricted",
        connection=("start", "restricted"),
        remaining_transit_turns=2,
    )
    drone = Drone(
        drone_id=1,
        current_hub="start",
        route=["start", "restricted", "goal"],
        status=DroneStatus.MOVING,
        transit=transit,
    )

    assert drone.transit == transit
    assert drone.transit.remaining_transit_turns == 2


def test_transit_requires_positive_remaining_turns() -> None:
    with pytest.raises(ValueError):
        TransitState(
            origin_hub="start",
            destination_hub="goal",
            connection=("start", "goal"),
            remaining_transit_turns=0,
        )
