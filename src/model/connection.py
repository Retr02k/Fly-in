from pydantic import BaseModel
from model.hub import Hub


class Connection(BaseModel):
    hub1: str
    hub2: str
    max_link_capacity: int = 1
