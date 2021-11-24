from pydantic import BaseModel


class Road(BaseModel):
    road_id: int
    name: str
