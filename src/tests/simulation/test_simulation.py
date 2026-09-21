from fly_in.parser.map_parser import MapParser
from fly_in.simulation.simulation import Simulator


def test_simulator_creates_one_drone_per_map_count():
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.drones) == drone_map.nb_drones
    assert all(
        drone.current_hub == drone_map.start_hub
        for drone in simulator.drones
    )
    assert all(
        drone.route == ["start", "waypoint1", "waypoint2", "goal"]
        for drone in simulator.drones
    )


def test_simulator_moves_all_drones_to_goal():
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)
    turns = simulator.run()

    assert len(turns) == 3
    assert simulator.current_turn == 3
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )
