from core.model.train import Train
from core.storage.sql_server import DB


class TrainStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, train_id: int) -> Train:
        sql = 'SELECT * from [Train] WHERE train_id = ?'
        row = await self.db.execute(sql, train_id)
        return Train.parse_obj(row[0])
