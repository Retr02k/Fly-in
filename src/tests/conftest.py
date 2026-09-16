import pytest


@pytest.fixture
def path_to_map_file():
    return "src/maps/medium/03_priority_puzzle.txt"


@pytest.fixture
def path_to_expected_output_file():
    return "src/tests/expected_outputs/medium/03_priority_puzzle.py"
