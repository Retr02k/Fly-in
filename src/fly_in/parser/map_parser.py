from typing import Callable
from pydantic import BaseModel
from model.map import Map
from parser.map_builder import MapBuilder


HANDLERS: dict[str, Callable[[MapBuilder, str], None]] = {}

def register(key: str):
    def decorator(fn):
        HANDLERS[key] = fn
        return fn
    return decorator


class MapParser(BaseModel):
    filepath: str

    def parse(self) -> Map:
        from parser import handlers  # noqa: F401 — triggers registration

        builder = MapBuilder()

        with open(self.filepath) as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                key, _, value = line.partition(":")
                key, value = key.strip(), value.strip()

                handler = HANDLERS.get(key)
                if handler is None:
                    raise ValueError(f"Unknown map directive: {key!r}")
                handler(builder, value)

        return builder.build()


try:
    parser = MapParser(filepath="src/maps/easy/01_linear_path.txt")
    drone_map = parser.parse()
except Exception as error:
    print(error)
