from dataclasses import dataclass, field
from fly_in.model.connection import Connection
from fly_in.model.hub import Hub
from fly_in.model.map import Map


@dataclass
class MapBuilder:
    """Accumulate parser results before constructing a validated map.

    The line metadata is retained so final validation failures can point to
    the most relevant declaration instead of the end of the source file.
    """
    nb_drones: int = 0
    hubs: dict[str, Hub] = field(default_factory=dict)
    connections: list[Connection] = field(default_factory=list)
    start_hub: str = ""
    end_hub: str = ""
    current_line: int = 0
    nb_drones_line: int = 0
    start_hub_line: int = 0
    end_hub_line: int = 0
    hub_lines: dict[str, int] = field(default_factory=dict)
    connection_lines: list[int] = field(default_factory=list)

    def build(self) -> Map:
        """Build a map model from the collected directives.

        Returns:
            A Pydantic map model containing the parsed data.
        """
        return Map(
            nb_drones=self.nb_drones,
            hubs=self.hubs,
            connections=self.connections,
            start_hub=self.start_hub,
            end_hub=self.end_hub,
        )
