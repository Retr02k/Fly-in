from pydantic import BaseModel
from model.hub import Hub
from model.connection import Connection


class Map(BaseModel):
    nb_drones: int
    hubs: dict[str, Hub]
    connections: list[Connection]
    start_hub: str
    end_hub: str
