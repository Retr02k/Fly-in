from fly_in.parser.map_parser import register
from fly_in.parser.map_builder import MapBuilder


@register("nb_drones")
def handle_nb_drones(builder: MapBuilder, value: str) -> None:
    builder.nb_drones = int(value)
