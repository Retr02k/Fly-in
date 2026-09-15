from pydantic import BaseModel
from fly_in.model.hub import Hub
from fly_in.model.connection import Connection


class Map(BaseModel):
    nb_drones: int
    hubs: dict[str, Hub]
    connections: list[Connection]
    start_hub: str
    end_hub: str
