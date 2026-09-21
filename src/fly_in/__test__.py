from fly_in import graph
import fly_in
from fly_in.model.hub import Hub
from fly_in.parser.map_parser import MapParser
from fly_in.parser.map_builder import MapBuilder
from fly_in.graph.builder import GraphBuilder
from fly_in.graph.pathfinding import GraphTraversal
from fly_in.simulation.simulation import Simulator


if __name__ == "__main__":
    parser = MapParser(filepath="src/maps/easy/01_linear_path.txt")
    drone_map = parser.parse()
    graph_builder = GraphBuilder(drone_map)
    matrix = graph_builder.hub_matrix()
    connections = graph_builder.connectors_dic()
    pathfinding = GraphTraversal(drone_map)
    bfs = pathfinding.bfs(connections, drone_map.start_hub, drone_map.end_hub)

    simulator = Simulator(drone_map)
    print("RUN")
    for run in simulator.run():
        for sub_run in run:
            print(sub_run)
