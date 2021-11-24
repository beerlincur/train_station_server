from typing import List, Optional

from core.api.registry import road_storage, road_station_storage, ticket_storage
from core.helpers.road_station import generate_road_station_response
from core.model.ticket import TicketResponse, Ticket


async def generate_tickets_response(tickets: List[Ticket]) -> List[TicketResponse]:
    result: List[TicketResponse] = []
    for t in tickets:
        result.append(
            TicketResponse(
                ticket_id=t.ticket_id,
                road=await road_storage.get_by_id(t.road_id),
                departure_station=await generate_road_station_response(t.departure_station_id, None),
                arrival_station=await generate_road_station_response(t.arrival_station_id, None),
                car_number=t.car_number,
                seat_number=t.seat_number,
                is_bought=t.is_bought,
                is_in_train=t.is_in_train,
                race_number=t.race_number,
                stations=await road_station_storage.get_between_ids(t.departure_station_id, t.arrival_station_id)
            )
        )

    return result


async def generate_ticket_response(ticket_id: int,
                                   ticket: Optional[Ticket]) -> TicketResponse:
    if ticket is None:
        ticket = await ticket_storage.get_by_id(ticket_id)
    return TicketResponse(
        ticket_id=ticket.ticket_id,
        road=await road_storage.get_by_id(ticket.road_id),
        departure_station=await generate_road_station_response(ticket.departure_station_id, None),
        arrival_station=await generate_road_station_response(ticket.arrival_station_id, None),
        car_number=ticket.car_number,
        seat_number=ticket.seat_number,
        is_bought=ticket.is_bought,
        is_in_train=ticket.is_in_train,
        race_number=ticket.race_number,
        stations=await road_station_storage.get_between_ids(ticket.departure_station_id, ticket.arrival_station_id)
    )
