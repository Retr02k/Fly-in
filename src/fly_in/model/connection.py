from pydantic import BaseModel
from fly_in.model.hub import Hub


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    max_link_capacity: int = 1
