from typing import List

from core.model.ticket import Ticket
from core.storage.sql_server import DB


class TicketStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_all_tickets(self) -> List[Ticket]:
        sql = 'SELECT * from [Ticket]'
        rows = await self.db.execute(sql)
        output: List[Ticket] = []
        for row in rows:
            output.append(Ticket.parse_obj(row))
        return output
