from core.model.station import Station
from core.storage.sql_server import DB


class StationStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, station_id: int) -> Station:
        sql = 'SELECT * from [Station] WHERE station_id = ?'
        row = await self.db.execute(sql, station_id)
        return Station.parse_obj(row[0])
