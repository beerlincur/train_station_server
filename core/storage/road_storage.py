from typing import List

from core.model.road import Road, RoadResponse
from core.model.station import Station
from core.storage.sql_server import DB


class RoadStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, road_id: int) -> Road:
        sql = 'SELECT * from [Road] WHERE road_id = ?'
        row = await self.db.execute(sql, road_id)
        return Road.parse_obj(row[0])

    async def get_all(self) -> List[RoadResponse]:
        sql = 'SELECT road_id, name FROM [Road]'
        rows = await self.db.execute(sql)
        output = []
        for r in rows:
            road_id = r['road_id']
            road_name = r['name']
            sql2 = 'SELECT rs.station_id, s.name FROM [RoadStation] as rs ' \
                   'JOIN [Station] as s ON s.station_id = rs.station_id ' \
                   'WHERE rs.road_id = ? ' \
                   'GROUP BY rs.station_id, rs.num_in_road, s.name ' \
                   'ORDER BY rs.num_in_road'
            rows = await self.db.execute(sql2, road_id)
            stations = []
            for station in rows:
                stations.append(
                    Station.parse_obj(station)
                )
            output.append(
                RoadResponse(
                    road_id=road_id,
                    name=road_name,
                    stations=stations
                )
            )
        return output
