from fly_in.parser import MapParser
from fly_in.simulation import Simulator

__all__ = ["MapParser", "Simulator"]


def main() -> None:
    """Start the interactive Fly-in command-line application."""
    from fly_in.cli import main as cli_main

    cli_main()
