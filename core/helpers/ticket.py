from typing import List

from core.api.registry import road_storage, road_station_storage
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
