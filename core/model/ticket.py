from typing import Optional

from pydantic import BaseModel


class Ticket(BaseModel):
    ticket_id: int
    road_id: int
    departure_station_id: int
    arrival_station_id: int
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool


class TicketResponse(BaseModel):
    ticket_id: int
    road_id: int
    departure_station_id: int
    arrival_station_id: int
    car_number: int
    seat_number: int
    is_bought: bool
    is_in_train: bool


class TicketRequest(BaseModel):
    road_id: Optional[int]
    departure_station_id: Optional[int]
    arrival_station_id: Optional[int]
    car_number: Optional[int]
    seat_number: Optional[int]
    is_bought: Optional[bool]
    is_in_train: Optional[bool]

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
