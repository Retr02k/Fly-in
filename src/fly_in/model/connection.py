from pydantic import BaseModel


class Connection(BaseModel):
    from_hub: str
    to_hub: str
    max_link_capacity: int = 1
