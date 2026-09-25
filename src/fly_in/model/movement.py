from pydantic import BaseModel
from fly_in.model.drone import Drone


class PlannedMove(BaseModel):
    drone: Drone
    origin_hub: str
    destination_hub: str
    connection: tuple[str, str]
    duration: int
