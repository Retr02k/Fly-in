from enum import Enum
from pydantic import BaseModel, Field


class DroneStatus(str, Enum):
    WAITING = "waiting"
    MOVING = "moving"
    DELIVERED = "delivered"


class Drone(BaseModel):
    drone_id: int = Field(gt=0)
    current_hub: str
    route: list[str] = Field(min_length=1)
    current_route_index: int = 0
    status: DroneStatus = DroneStatus.WAITING
