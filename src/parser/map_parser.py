from pydantic import BaseModel, Field
from model.map import Map
from model.hub import Hub
from model.connection import Connection

class MapParser(BaseModel):
    filepath: str
    name: str = ""
    drone_number: int = 0
    difficulty: str = ""
    selected_map: Map | None = None
    hub_list: list[Hub] = Field(default_factory=lambda: list())

    def parse(self) -> Map:
        new_dict = {}

        with open(self.filepath) as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                key, _, value = line.partition(":")
                key = key.strip()
                value = value.strip()
                new_dict[key] = value

        self.drone_number = new_dict.get("nb_drones", 0)
        print(new_dict)

    def _parse_hub_lines(self, value: str) -> Hub:
        pass

    def _parse_connection_line(self, value: str) -> Connection:
        pass


try:
    parser = MapParser(filepath="src/maps/easy/01_linear_path.txt")
    drone_map = parser.parse()
except Exception as error:
    print(error)
