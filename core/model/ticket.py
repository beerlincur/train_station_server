from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel

from core.model.road import Road
from core.model.road_station import RoadStationResponse, RoadStationTicketResponse
from core.model.user import User


class Ticket(BaseModel):
    ticket_id: int
    road_id: int
    departure_station_id: int
    arrival_station_id: int
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool
    race_number: int


class TicketResponse(BaseModel):
    ticket_id: int
    road: Road
    departure_station: RoadStationResponse
    arrival_station: RoadStationResponse
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool
    race_number: int
    stations: List[RoadStationTicketResponse]


class TicketRequest(BaseModel):
    road_id: Optional[int]
    departure_station_id: Optional[int]
    arrival_station_id: Optional[int]
    car_number: Optional[int]
    seat_number: Optional[int]
    is_bought: Optional[bool]
    is_in_train: Optional[bool]
    race_number: Optional[int]

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
        if self.race_number:
            ticket.race_number = self.race_number


class TicketRaceResponse(BaseModel):
    ticket_id: int
    departure_station_name: str
    departure_station_time: datetime
    arrival_station_name: str
    arrival_station_time: datetime
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool


class TicketConductorResponse(BaseModel):
    ticket_id: int
    departure_station_name: str
    arrival_station_name: str
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool
    order_order_id: int
    order_created_at: datetime
    order_is_canceled: bool
    user_first_name: str
    user_second_name: str
    user_passport: str


class TicketSetInTrainRequest(BaseModel):
    ticket_id: int


