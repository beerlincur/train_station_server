from typing import List, Optional

from core.api.registry import road_station_storage, road_storage, station_storage, train_storage
from core.model.road_station import RoadStationResponse, RoadStation


async def generate_road_station_response(road_station_id: int,
                                         road_station: Optional[RoadStation]) -> RoadStationResponse:
    if road_station is None and road_station_id is not None:
        road_station = await road_station_storage.get_by_id(road_station_id)

    return RoadStationResponse(
            road_station_id=road_station.road_station_id,
            road=await road_storage.get_by_id(road_station.road_id),
            station=await station_storage.get_by_id(road_station.station_id),
            train=await train_storage.get_by_id(road_station.train_id),
            num_in_road=road_station.num_in_road,
            arrival_time=road_station.arrival_time,
            departure_time=road_station.departure_time,
            road_number=road_station.road_number
        )
