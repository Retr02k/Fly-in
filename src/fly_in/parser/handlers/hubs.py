import re
from parser.map_parser import register
from parser.map_builder import MapBuilder
from model.hub import Hub


def _parse_hub_fields(value: str) -> Hub:
    match = re.match(r"(\S+)\s+(-?\d+)\s+(-?\d+)\s*(?:\[(.*)\])?", value)
    name, x, y = match.group(1), int(match.group(2)), int(match.group(3))
    settings = dict(re.findall(r"(\w+)=(\w+)", match.group(4) or ""))
    return Hub(
        name=name, x=x, y=y,
        zone_type=settings.get("zone", "normal"),
        color=settings.get("color"),
        max_drones=int(settings.get("max_drones", 1)),
    )

@register("start_hub")
def handle_start_hub(builder: MapBuilder, value: str) -> None:
    hub = _parse_hub_fields(value)
    builder.hubs[hub.name] = hub
    builder.start_hub = hub.name

@register("end_hub")
def handle_end_hub(builder: MapBuilder, value: str) -> None:
    hub = _parse_hub_fields(value)
    builder.hubs[hub.name] = hub
    builder.end_hub = hub.name

@register("hub")
def handle_hub(builder: MapBuilder, value: str) -> None:
    hub = _parse_hub_fields(value)
    builder.hubs[hub.name] = hub
