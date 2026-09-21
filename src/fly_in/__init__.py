from fly_in.parser import MapParser
from fly_in.simulation import Simulator


def main() -> None:
    parsed_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()
    sim = Simulator(parsed_map)
    print(sim._allowed_drones_to_move())
