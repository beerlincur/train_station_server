from typing import List

from core.model.road_station import RoadStation, TicketRoadResponse
from core.storage.sql_server import DB


class RoadStationStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, road_station_id: int) -> RoadStation:
        sql = 'SELECT * from [RoadStation] WHERE road_station_id = ?'
        row = await self.db.execute(sql, road_station_id)
        return RoadStation.parse_obj(row[0])

    async def get_between_ids(self, departure_rs_id: int, arrival_rs_id: int) -> List[TicketRoadResponse]:
        sql = 'SELECT s.station_id, s.name, rs.departure_time, rs.arrival_time FROM [RoadStation] as rs ' \
              'JOIN [Station] as s ON s.station_id = rs.station_id ' \
              'WHERE rs.road_station_id >= ? AND rs.road_station_id <= ? ' \
              'ORDER BY rs.road_station_id'
        rows = await self.db.execute(sql, departure_rs_id, arrival_rs_id)
        output = []
        for row in rows:
            output.append(TicketRoadResponse.parse_obj(row))
        return output
