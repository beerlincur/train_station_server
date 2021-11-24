from typing import Optional, List

from pydantic import BaseModel

from core.model.road import Road
from core.model.road_station import RoadStationResponse, TicketRoadResponse
from core.model.station import Station


class Ticket(BaseModel):
    ticket_id: int
    road_id: int
    departure_station_id: int
    arrival_station_id: int
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool
    road_number: int


class TicketResponse(BaseModel):
    ticket_id: int
    road: Road
    departure_station: RoadStationResponse
    arrival_station: RoadStationResponse
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool
    road_number: int
    stations: List[TicketRoadResponse]


class TicketRequest(BaseModel):
    road_id: Optional[int]
    departure_station_id: Optional[int]
    arrival_station_id: Optional[int]
    car_number: Optional[int]
    seat_number: Optional[int]
    is_bought: Optional[bool]
    is_in_train: Optional[bool]
    road_number: Optional[int]

    def update_ticket(self, ticket: Ticket) -> None:
        if self.road_id:
            ticket.road_id = self.road_id
        if self.departure_station_id:
            ticket.departure_station_id = self.departure_station_id
        if self.arrival_station_id:
            ticket.arrival_station_id = self.arrival_station_id
        if self.car_number:
            ticket.car_number = self.car_number
        if self.seat_number:
            ticket.seat_number = self.seat_number
        if self.is_bought is not None:
            ticket.is_bought = self.is_bought
        if self.is_in_train is not None:
            ticket.is_in_train = self.is_in_train
        if self.road_number:
            ticket.road_number = self.road_number
