from typing import List

from core.utils.utils import throw_server_error
from core.storage.sql_server import DB


class PingStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def ping(self):
        cursor = await self.db.execute("SELECT 'pong' AS pong")
        for row in cursor:
            return row['pong']
        throw_server_error('Unable to ping db')
