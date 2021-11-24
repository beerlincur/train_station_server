from core.model.road import Road
from core.storage.sql_server import DB


class RoadStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, road_id: int) -> Road:
        sql = 'SELECT * from [Road] WHERE road_id = ?'
        row = await self.db.execute(sql, road_id)
        return Road.parse_obj(row[0])
