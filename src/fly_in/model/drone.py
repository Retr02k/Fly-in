from enum import Enum
from pydantic import BaseModel, Field
from fly_in.model.transit import TransitState


class DroneStatus(str, Enum):
    """Describe the lifecycle state of a drone."""

    WAITING = "waiting"
    MOVING = "moving"
    DELIVERED = "delivered"


class Drone(BaseModel):
    """Represent a drone and its current route state.

    Attributes:
        drone_id: Positive identifier used for deterministic scheduling.
        current_hub: Last hub physically occupied by the drone.
        route: Ordered route from the start hub to the goal.
        current_route_index: Index of the last reached route hub.
        status: Current lifecycle state.
        transit: Active connection movement, when applicable.
    """
    drone_id: int = Field(gt=0)
    current_hub: str
    route: list[str] = Field(min_length=1)
    current_route_index: int = 0
    status: DroneStatus = DroneStatus.WAITING
    transit: TransitState | None = None
