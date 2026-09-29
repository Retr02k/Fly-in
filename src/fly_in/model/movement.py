from pydantic import BaseModel
from fly_in.model.drone import Drone


class PlannedMove(BaseModel):
    """Describe a movement approved during turn planning.

    Attributes:
        drone: Drone selected for the movement.
        origin_hub: Departure hub.
        destination_hub: Reserved arrival hub.
        connection: Link occupied by the movement.
        duration: Number of turns required for arrival.
    """
    drone: Drone
    origin_hub: str
    destination_hub: str
    connection: tuple[str, str]
    duration: int
