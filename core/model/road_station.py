from datetime import datetime

from pydantic import BaseModel

from core.model.road import Road
from core.model.station import Station
from core.model.train import Train


class RoadStation(BaseModel):
    road_station_id: int
    road_id: int
    station_id: int
    train_id: int
    num_in_road: int
    arrival_time: datetime
    departure_time: datetime
    race_number: int


class RoadStationResponse(BaseModel):
    road_station_id: int
    road: Road
    station: Station
    train: Train
    num_in_road: int
    arrival_time: datetime
    departure_time: datetime
    race_number: int


class TicketRoadResponse(BaseModel):
    station_id: int
    name: str
    departure_time: datetime
    arrival_time: datetime


class RoadStationRaceResponse(BaseModel):
    road_station_id: int
    station: Station
    num_in_road: int
    arrival_time: datetime
    departure_time: datetime
