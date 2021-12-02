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

    async def get_id_by_race_number(self, race_number: int) -> int:
        sql = 'SELECT TOP 1 road_id FROM [RoadStation] WHERE race_number = ?'
        rows = await self.db.execute(sql, race_number)
        return rows[0]['road_id']

    async def get_all(self) -> List[RoadResponse]:
        sql = 'SELECT r.road_id, r.name, COUNT(o.order_id) AS count ' \
                'FROM [Road] AS r ' \
                'LEFT JOIN [Ticket] AS t ON t.road_id = r.road_id ' \
                'LEFT JOIN [Order] AS o ON o.ticket_id = t.ticket_id AND o.is_canceled = 0 ' \
                'GROUP BY r.road_id, r.name ' \
                'ORDER BY COUNT(o.order_id) DESC'
        rows = await self.db.execute(sql)
        output = []
        for r in rows:
            road_id = r['road_id']
            road_name = r['name']
            order_count = r['count']
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
                    stations=stations,
                    amount_of_orders=order_count
                )
            )
        return output

    async def create(self, name) -> None:
        sql = 'INSERT INTO [Road] VALUES (?)'
        row = await self.db.execute(sql, name)
