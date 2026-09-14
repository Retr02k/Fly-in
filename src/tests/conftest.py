import pytest

MAP_CONTENT = """\
# Easy Level 1: Simple linear path
nb_drones: 2

start_hub: start 0 0 [zone=normal color=green max_drones=5]
hub: waypoint1 1 0 [color=blue]
hub: waypoint2 2 0 [color=blue]
end_hub: goal 3 0 [zone=normal color=red max_drones=1]

connection: start-waypoint1
connection: waypoint1-waypoint2
connection: waypoint2-goal
"""

@pytest.fixture
def map_file(tmp_path):
    path = tmp_path / "level1.map"
    path.write_text(MAP_CONTENT)
    return str(path)
