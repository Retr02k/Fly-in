from dataclasses import dataclass, field
from model.connection import Connection
from model.hub import Hub
from model.map import Map

@dataclass
class MapBuilder:
    nb_drones: int = 0
    hubs: dict[str, Hub] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
    start_hub: str = ""
    end_hub: str = ""

    def build(self) -> Map:
        return Map(
            nb_drones=self.nb_drones,
            hubs=self.hubs,
            connections=self.connections,
            start_hub=self.start_hub,
            end_hub=self.end_hub,
        )
