from typing import List

from core.model.station import Station
from core.storage.sql_server import DB


class StationStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, station_id: int) -> Station:
        sql = 'SELECT * from [Station] WHERE station_id = ?'
        row = await self.db.execute(sql, station_id)
        return Station.parse_obj(row[0])

    async def get_all(self) -> List[Station]:
        sql = 'SELECT * from [Station] ORDER BY station_id'
        rows = await self.db.execute(sql)
        output = []
        for row in rows:
            output.append(
                Station.parse_obj(row)
            )
        return output
