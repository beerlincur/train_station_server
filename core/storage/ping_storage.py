from typing import List

from pydantic import BaseModel

from core.utils.utils import throw_server_error
from core.storage.sql_server import DB


class Hello(BaseModel):
    user_id: int
    first_name: str


class PingStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def ping(self):
        cursor = await self.db.execute("SELECT 'pong' AS pong")
        for row in cursor:
            return row['pong']
        throw_server_error('Unable to ping db')

    async def get_all_hello(self):
        sql = 'SELECT * FROM hello'
        rows = await self.db.execute(sql)
        output: List[Hello] = []
        for row in rows:
            output.append(Hello.parse_obj(row))
        return output

    async def get_value_hello(self):
        sql = 'SELECT first_name FROM hello where user_id=1'
        rows = await self.db.execute(sql)
        print(rows)
        # output: List[Hello] = []
        # for row in rows:
        #     output.append(Hello.parse_obj(row))
        return rows[0]['first_name']
