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

    async def set_is_in_train(self, is_in_train: int, ticket_id: int) -> None:
        sql = 'UPDATE [Ticket] SET is_in_train = ? WHERE ticket_id = ?'
        row = await self.db.execute(sql, is_in_train, ticket_id)

    async def create(self,
                     road_id: int,
                     departure_station_id: int,
                     arrival_station_id: int,
                     car_number: int,
                     seat_number: int,
                     race_number: int) -> None:
        sql = 'INSERT INTO [Ticket] (road_id,' \
              'departure_station_id,' \
              'arrival_station_id,' \
              'car_number,' \
              'seat_number,' \
              'is_bought,' \
              'is_in_train,' \
              'race_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'

        await self.db.execute(sql,
                              road_id,
                              departure_station_id,
                              arrival_station_id,
                              car_number,
                              seat_number,
                              False,
                              False,
                              race_number)
