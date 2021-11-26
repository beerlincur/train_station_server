from typing import List

from pydantic import BaseModel

from core.model.station import Station


class Road(BaseModel):
    road_id: int
    name: str


class RoadResponse(BaseModel):
    road_id: int
    name: str
    stations: List[Station]
