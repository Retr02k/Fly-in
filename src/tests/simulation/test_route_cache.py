from fly_in.parser import MapParser
from fly_in.simulation import Simulator


def test_simulator_reuses_routes_for_repeated_origins() -> None:
    parsed_map = MapParser(
        filepath="src/maps/easy/01_linear_path.txt"
    ).parse()
    simulator = Simulator(parsed_map)

    initial_misses = simulator.route_cache_misses
    simulator.run()

    assert simulator.route_cache_misses > initial_misses
    assert simulator.route_cache_misses == 3
    assert simulator.route_cache_hits > 0
