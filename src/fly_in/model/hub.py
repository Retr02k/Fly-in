from fly_in.header.header import ZoneType
from pydantic import BaseModel, Field


class Hub(BaseModel):
    name: str = Field(min_length=1)
    x: int = Field(default=0)
    y: int = Field(default=0)
    zone_type: ZoneType = ZoneType.NORMAL
    color: str | None = None
    max_drones: int = 1
