from typing import List

from core.model.ticket import Ticket
from core.storage.sql_server import DB


class TicketStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_all_tickets(self):
        sql = 'SELECT * from [Ticket] WHERE is_bought = 0'
        rows = await self.db.execute(sql)
        output: List[Ticket] = []
        for row in rows:
            output.append(Ticket.parse_obj(row))
        return output
