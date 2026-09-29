from pydantic import BaseModel, Field


class Connection(BaseModel):
    """Represent a bidirectional connection between two hubs.

    Attributes:
        from_hub: Name of one endpoint.
        to_hub: Name of the other endpoint.
        max_link_capacity: Number of drones allowed on the link at once.
    """

    from_hub: str
    to_hub: str
    max_link_capacity: int = Field(default=1, gt=0)
