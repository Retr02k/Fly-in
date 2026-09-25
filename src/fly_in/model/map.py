from pydantic import BaseModel, Field, model_validator
from fly_in.model.hub import Hub
from fly_in.model.connection import Connection


class Map(BaseModel):
    nb_drones: int = Field(gt=0)
    hubs: dict[str, Hub]
    connections: list[Connection]
    start_hub: str
    end_hub: str

    @model_validator(mode="after")
    def validate_structure(self) -> "Map":
        if self.start_hub == self.end_hub:
            raise ValueError("start and end hubs must be different")
        if self.start_hub not in self.hubs:
            raise ValueError(f"Unknown start hub: {self.start_hub!r}")
        if self.end_hub not in self.hubs:
            raise ValueError(f"Unknown end hub: {self.end_hub!r}")

        return self
