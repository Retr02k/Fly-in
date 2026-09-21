import pytest


@pytest.fixture
def path_to_map_file() -> str:
    return "src/maps/easy/01_linear_path.txt"


@pytest.fixture
def path_to_expected_output_file() -> str:
    return "src/tests/expected_outputs/easy/01_linear_path.py"
