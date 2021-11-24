from datetime import datetime
from typing import List

from core.model.order import Order
from core.storage.sql_server import DB


class OrderStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def create(self, user_id: int, ticket_id: int) -> None:
        sql = 'INSERT INTO [Order] (user_id, ticket_id, is_canceled, created_at) VALUES (?, ?, ?, ?)'
        row = await self.db.execute(sql,
                                    user_id,
                                    ticket_id,
                                    False,
                                    datetime.now())
        sql2 = 'UPDATE [Ticket] SET is_bought = 1 WHERE ticket_id = ?'
        row = await self.db.execute(sql2, ticket_id)

    async def get_by_user_id(self, user_id: int) -> List[Order]:
        sql = 'SELECT * FROM [Order] WHERE user_id = ? ORDER BY created_at DESC'
        rows = await self.db.execute(sql, user_id)
        output = []
        for row in rows:
            output.append(
                Order.parse_obj(row)
            )
        return output
