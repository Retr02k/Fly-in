from pydantic import BaseModel, Field
from fly_in.model.zone import ZoneType


class Hub(BaseModel):
    """Represent a map hub and its movement constraints.

    Attributes:
        name: Unique hub name.
        x: Horizontal map coordinate.
        y: Vertical map coordinate.
        zone_type: Movement behavior and route cost for this hub.
        color: Optional display color metadata.
        max_drones: Number of active drones the hub can hold.
    """

    name: str = Field(min_length=1)
    x: int = Field(default=0)
    y: int = Field(default=0)
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = Field(default=1, gt=0)
