from typing import List

from pydantic import BaseModel

from core.model.road import Road
from core.model.road_station import RoadStationRaceResponse
from core.model.ticket import TicketRaceResponse, TicketConductorResponse
from core.model.train import Train


class RaceResponse(BaseModel):
    race_number: int
    road: Road
    train: Train
    stations: List[RoadStationRaceResponse]
    tickets: List[TicketRaceResponse]


class RaceConductorResponse(BaseModel):
    race_number: int
    road: Road
    train: Train
    stations: List[RoadStationRaceResponse]
    tickets: List[TicketConductorResponse]

