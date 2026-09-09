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
                match key:
                    case "start_hub" | "end_hub":
                        endpoint_hub = self._parse_endpoint_hub(value)
                    case "start_hub" | "end_hub" | "hub":
                        hub = self._parse_hub_line(value)
                        self.hub_list.append(hub)
                    case "connection":
                        connection = self._parse_connection_line(value)

                new_dict[key] = value

        self.drone_number = new_dict.get("nb_drones", 0)
        #print(new_dict)
        #print(f'\n\n=== Start Hub ===\n{new_dict.get("start_hub")}\n')
        #print(f'=== End Hub ===\n{new_dict.get("end_hub")}\n')
        #print(f'=== Hub ===\n{new_dict.get("hub")}')


    def _parse_hub_line(self, value: str) -> Hub:
        pass

    def _parse_connection_line(self, value: str) -> Connection:
        pass

    def _parse_endpoint_hub(self, value: str) -> Hub:
        print(value)
        name, x, y, zone_type, color, max_drone = value.split()
        gabriel = Hub(name=name, x=x, y=y)


try:
    parser = MapParser(filepath="src/maps/easy/01_linear_path.txt")
    drone_map = parser.parse()
except Exception as error:
    print(error)
