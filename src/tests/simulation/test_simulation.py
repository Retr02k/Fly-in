from fly_in.parser.map_parser import MapParser
from fly_in.simulation.simulation import Simulator


def test_simulator_creates_one_drone_per_map_count() -> None:
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


def test_simulator_moves_all_drones_to_goal() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()

    simulator = Simulator(drone_map)
    turns = simulator.run()

    assert len(turns) == 5
    assert simulator.current_turn == 5
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )


def test_simulator_respects_hub_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/03_basic_capacity.txt"
    ).parse()

    simulator = Simulator(drone_map)
    simulator.step()

    assert sum(
        drone.transit is not None
        and drone.transit.destination_hub == "bottleneck"
        for drone in simulator.drones
    ) == 2


def test_simulator_respects_link_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/medium/03_priority_puzzle.txt"
    ).parse()

    simulator = Simulator(drone_map)
    simulator.step()
    simulator.step()
    third_turn = simulator.step()

    assert sum(
        destination == "goal"
        for _, _, destination in third_turn
    ) <= 2
