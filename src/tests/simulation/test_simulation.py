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


def test_simulator_treats_end_hub_as_unlimited_sink() -> None:
    drone_map = MapParser(
        filepath="src/maps/easy/03_basic_capacity.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.run()) <= 6
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )


def test_circular_loop_preserves_restricted_link_capacity() -> None:
    drone_map = MapParser(
        filepath="src/maps/medium/02_circular_loop.txt"
    ).parse()

    simulator = Simulator(drone_map)
    restricted_departures: list[int] = []

    while any(drone.status.value != "delivered" for drone in simulator.drones):
        simulator.step()
        restricted_departures.extend(
            simulator.current_turn
            for move in simulator.last_planned_moves
            if move.destination_hub == "exit_point"
        )

    assert restricted_departures == [3, 5, 7, 9, 11, 13]
    assert simulator.current_turn == 16


def test_edge_case_map_waits_until_capacity_is_available() -> None:
    drone_map = MapParser(
        filepath="src/maps/test_edge_cases.txt"
    ).parse()

    simulator = Simulator(drone_map)

    assert len(simulator.run()) == 9
    assert all(
        drone.current_hub == drone_map.end_hub
        for drone in simulator.drones
    )
