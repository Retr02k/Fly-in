from pydantic import BaseModel, Field


class TransitState(BaseModel):
    origin_hub: str
    destination_hub: str
    connection: tuple[str, str]
    remaining_transit_turns: int = Field(gt=0)
