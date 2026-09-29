from fly_in.parser.map_parser import register
from fly_in.parser.map_builder import MapBuilder


@register("nb_drones")
def handle_nb_drones(builder: MapBuilder, value: str) -> None:
    """Parse and validate the number of drones directive.

    Args:
        builder: Parser state being populated.
        value: Text following the ``nb_drones:`` directive.

    Raises:
        ValueError: If the value is not a positive integer.
    """
    try:
        nb_drones = int(value)
    except ValueError as error:
        raise ValueError(
            f"nb_drones must be a valid integer, got {value!r}"
        ) from error
    if nb_drones <= 0:
        raise ValueError("nb_drones must be greater than zero")
    builder.nb_drones = nb_drones
    builder.nb_drones_line = builder.current_line
