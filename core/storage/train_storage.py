from typing import List

from core.model.train import Train
from core.storage.sql_server import DB


class TrainStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, train_id: int) -> Train:
        sql = 'SELECT * from [Train] WHERE train_id = ?'
        row = await self.db.execute(sql, train_id)
        return Train.parse_obj(row[0])

    async def get_all(self) -> List[Train]:
        sql = 'SELECT * from [Train] ORDER BY train_id'
        rows = await self.db.execute(sql)
        output = []
        for row in rows:
            output.append(
                Train.parse_obj(row)
            )
        return output

    async def create(self, name) -> None:
        sql = 'INSERT INTO [Train] VALUES (?)'
        row = await self.db.execute(sql, name)
