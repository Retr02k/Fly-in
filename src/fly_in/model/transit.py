from pydantic import BaseModel, Field


class TransitState(BaseModel):
    """Represent a drone travelling between two hubs.

    Attributes:
        origin_hub: Hub from which the drone departed.
        destination_hub: Hub reserved for arrival.
        connection: Endpoint names identifying the occupied link.
        remaining_transit_turns: Turns until the drone arrives.
    """
    origin_hub: str
    destination_hub: str
    connection: tuple[str, str]
    remaining_transit_turns: int = Field(gt=0)
