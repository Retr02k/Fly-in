import re
from fly_in.parser.map_parser import register
from fly_in.parser.map_builder import MapBuilder
from fly_in.model.hub import Hub


def _parse_hub_fields(value: str) -> Hub:
    """Parse a hub declaration into a typed hub model.

    Args:
        value: Hub name, coordinates, and optional settings.

    Returns:
        The parsed hub.

    Raises:
        ValueError: If coordinates or settings are invalid.
    """
    match = re.fullmatch(
        r"(?P<name>\S+)\s+(?P<x>\S+)\s+(?P<y>\S+)"
        r"\s*(?:\[(?P<settings>.*)\])?",
        value,
    )
    if match is None:
        raise ValueError(
            "hub syntax must be: name integer integer [settings]"
        )

    name = match.group("name")
    try:
        x = int(match.group("x"))
        y = int(match.group("y"))
    except ValueError as error:
        raise ValueError("hub coordinates x and y must be integers") from error
    settings = dict(re.findall(r"(\w+)=(\w+)", match.group("settings") or ""))
    try:
        max_drones = int(settings.get("max_drones", 1))
    except ValueError as error:
        raise ValueError("max_drones must be a valid integer") from error
    return Hub(
        name=name, x=x, y=y,
        zone_type=settings.get("zone", "normal"),
        color=settings.get("color"),
        max_drones=max_drones,
    )


def _ensure_unique_hub(builder: MapBuilder, hub: Hub) -> None:
    """Ensure a hub name and coordinates are unique in the map.

    Args:
        builder: Parser state containing previously declared hubs.
        hub: Newly parsed hub to validate.

    Raises:
        ValueError: If the name or coordinates are already used.
    """
    if hub.name in builder.hubs:
        raise ValueError(f"Duplicate hub name: {hub.name!r}")
    for other_name, other_hub in builder.hubs.items():
        if (hub.x, hub.y) == (other_hub.x, other_hub.y):
            raise ValueError(
                f"hub {hub.name!r} has the same coordinates as "
                f"hub {other_name!r}"
            )


@register("start_hub")
def handle_start_hub(builder: MapBuilder, value: str) -> None:
    """Parse the single allowed start-hub declaration."""
    if builder.start_hub:
        raise ValueError("exactly one start_hub is allowed")
    hub = _parse_hub_fields(value)
    _ensure_unique_hub(builder, hub)
    builder.hubs[hub.name] = hub
    builder.start_hub = hub.name
    builder.start_hub_line = builder.current_line
    builder.hub_lines[hub.name] = builder.current_line


@register("end_hub")
def handle_end_hub(builder: MapBuilder, value: str) -> None:
    """Parse the single allowed end-hub declaration."""
    if builder.end_hub:
        raise ValueError("exactly one end_hub is allowed")
    hub = _parse_hub_fields(value)
    _ensure_unique_hub(builder, hub)
    builder.hubs[hub.name] = hub
    builder.end_hub = hub.name
    builder.end_hub_line = builder.current_line
    builder.hub_lines[hub.name] = builder.current_line


@register("hub")
def handle_hub(builder: MapBuilder, value: str) -> None:
    """Parse and add a regular hub declaration."""
    hub = _parse_hub_fields(value)
    _ensure_unique_hub(builder, hub)
    builder.hubs[hub.name] = hub
    builder.hub_lines[hub.name] = builder.current_line
