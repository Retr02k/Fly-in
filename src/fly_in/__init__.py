from fly_in.graph.builder import GraphBuilder
from fly_in.graph.pathfinding import GraphTraversal
from fly_in.parser import MapParser
from fly_in.simulation import Simulator

__all__ = ["MapParser", "Simulator"]


def main() -> None:
    parsed_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()
    traversal = GraphTraversal(parsed_map)
    neighbors = GraphBuilder(parsed_map).connectors_dic()
    print(
        traversal.find_best_route(
            neighbors,
            parsed_map.hubs,
            parsed_map.start_hub,
            parsed_map.end_hub,
        )
    )
