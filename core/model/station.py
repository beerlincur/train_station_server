from pydantic import BaseModel


class Station(BaseModel):
    station_id: int
    name: str


class StationCreateRequest(BaseModel):
    name: str
