from typing import List

from core.model.ticket import Ticket
from core.storage.sql_server import DB


class TicketStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_all_tickets(self) -> List[Ticket]:
        sql = 'SELECT * FROM [Ticket]'
        rows = await self.db.execute(sql)
        output: List[Ticket] = []
        for row in rows:
            output.append(Ticket.parse_obj(row))
        return output

    async def get_by_race_id(self, race_id: int) -> List[Ticket]:
        sql = 'SELECT * FROM [Ticket] WHERE race_number = ?'
        rows = await self.db.execute(sql, race_id)
        output: List[Ticket] = []
        for row in rows:
            output.append(Ticket.parse_obj(row))
        return output

    async def get_by_id(self, ticket_id: int) -> Ticket:
        sql = 'SELECT * FROM [Ticket] WHERE ticket_id = ?'
        row = await self.db.execute(sql, ticket_id)

        return Ticket.parse_obj(row[0])

    async def set_is_in_train(self, ticket_id: int) -> None:
        sql = 'UPDATE [Ticket] SET is_in_train = 1 WHERE ticket_id = ?'
        row = await self.db.execute(sql, ticket_id)
