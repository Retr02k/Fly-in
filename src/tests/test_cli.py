from io import StringIO
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

import fly_in.cli as cli
from fly_in.cli import _choose_map
from fly_in.model.drone import DroneStatus


def test_cli_runs_map_and_reports_delivery(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = StringIO()
    map_path = (
        Path(__file__).resolve().parents[1]
        / "maps/easy/01_linear_path.txt"
    )
    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO(f"c\n{map_path}\n1\nn\n"),
    )
    monkeypatch.setattr(sys, "stdout", output)
    with pytest.raises(SystemExit) as error:
        cli.main()

    rendered = output.getvalue()
    assert error.value.code == 0
    assert "Turn 1 movement events:" in rendered
    assert "D1 moved start -> waypoint1 (arrived this turn)." in rendered
    assert "D1 arrived at goal" in rendered
    assert "Delivered 2 drones" in rendered
    assert "Simulation statistics" in rendered


def test_cli_overwrites_requested_log(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    log_path = Path("simulation.log")
    log_path.write_text("old content")
    map_path = (
        Path(__file__).resolve().parents[2]
        / "src/maps/easy/01_linear_path.txt"
    )

    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO(f"c\n{map_path}\n1\ny\nsimulation.log\n"),
    )
    monkeypatch.setattr(sys, "stdout", StringIO())
    with pytest.raises(SystemExit) as error:
        cli.main()
    assert error.value.code == 0

    content = (tmp_path / "output" / "simulation.log").read_text()
    assert "old content" not in content
    assert "Delivered 2 drones in 4 turns." in content


def test_custom_map_selection_prompts_for_path() -> None:
    output = StringIO()
    selected = _choose_map(
        StringIO("c\nsrc/maps/easy/01_linear_path.txt\n"),
        output,
    )

    assert selected == "src/maps/easy/01_linear_path.txt"
    assert "Enter the path to the map file:" in output.getvalue()


def test_log_path_cannot_escape_output_directory(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    output = StringIO()

    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO("1\n1\ny\n../unsafe.log\n"),
    )
    monkeypatch.setattr(sys, "stdout", output)
    with pytest.raises(SystemExit) as error:
        cli.main()
    assert error.value.code == (
        "Unable to run simulation: "
        "Log path must stay inside the output directory."
    )


def test_cli_handles_keyboard_interrupt_and_closes_log(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class InterruptingSimulator:
        def __init__(self, parsed_map: object) -> None:
            self.parsed_map = parsed_map
            self.current_turn = 0
            self.drones = [
                SimpleNamespace(
                    drone_id=1,
                    status=DroneStatus.WAITING,
                    current_hub="start",
                ),
            ]

        def step(self) -> None:
            raise KeyboardInterrupt

    monkeypatch.setattr(cli, "Simulator", InterruptingSimulator)
    monkeypatch.chdir(tmp_path)
    output = StringIO()
    map_path = (
        Path(__file__).resolve().parents[2]
        / "src/maps/easy/01_linear_path.txt"
    )
    monkeypatch.setattr(
        sys,
        "stdin",
        StringIO(
            "c\n"
            f"{map_path}\n"
            "1\ny\ninterrupted.log\n"
        ),
    )
    monkeypatch.setattr(sys, "stdout", output)
    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 130
    assert "Simulation interrupted by user." in output.getvalue()
    log = tmp_path / "output" / "interrupted.log"
    log_content = log.read_text()
    assert "Turn 0 | start -> goal" in log_content
    assert log_content.endswith("Simulation interrupted by user.\n")
