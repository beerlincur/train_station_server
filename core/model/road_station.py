from datetime import datetime

from pydantic import BaseModel


class RoadStation(BaseModel):
    road_station_id: int
    road_id: int
    station_id: int
    train_id: int
    num_in_road: int
    arrival_time: datetime
    departure_time: datetime
    road_number: int
