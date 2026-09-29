from pydantic import BaseModel, Field, model_validator
from fly_in.model.hub import Hub
from fly_in.model.connection import Connection


class Map(BaseModel):
    """Represent a validated drone map.

    Attributes:
        nb_drones: Number of drones created for the simulation.
        hubs: Hub definitions indexed by name.
        connections: Bidirectional links between hubs.
        start_hub: Name of the unique departure hub.
        end_hub: Name of the unique delivery hub.
    """
    nb_drones: int = Field(gt=0)
    hubs: dict[str, Hub]
    connections: list[Connection]
    start_hub: str
    end_hub: str

    @model_validator(mode="after")
    def validate_structure(self) -> "Map":
        """Validate start/end references and their relationship.

        Returns:
            The validated map instance.

        Raises:
            ValueError: If start or end references are invalid.
        """
        if self.start_hub == self.end_hub:
            raise ValueError("start and end hubs must be different")
        if self.start_hub not in self.hubs:
            raise ValueError(f"Unknown start hub: {self.start_hub!r}")
        if self.end_hub not in self.hubs:
            raise ValueError(f"Unknown end hub: {self.end_hub!r}")

        return self
