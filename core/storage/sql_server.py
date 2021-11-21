import logging
import os
import time
from abc import ABC, abstractmethod
from typing import List

import aioodbc

from core.utils.utils import throw_server_error

LIMIT_RETRIES = 5


class DB(ABC):
    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def execute(self, query: str, *args):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


def get_database() -> DB:
    return AsyncDB(os.getenv('DATABASE_URL'))


class AsyncDB(DB):
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._cursor = None

        self._connection_pool = None

    async def connect(self, retry_counter=0) -> None:
        if not self._connection_pool:
            try:
                self._connection_pool = await aioodbc.create_pool(
                    minsize=1,
                    maxsize=20,
                    dsn=self.dsn
                )
                retry_counter = 0
                logging.info("Database pool connection opened")
            except Exception as error:
                if retry_counter >= LIMIT_RETRIES:
                    raise error
                retry_counter += 1
                logging.exception("got error {}. reconnecting {}".format(str(error).strip(), retry_counter))
                time.sleep(5)
                await self.connect()

    async def __check_connection(self):
        if not self._connection_pool:
            await self.connect()
        return await self._connection_pool.acquire()

    async def execute(self, query: str, *args):
        con = await self.__check_connection()
        try:
            async with con.cursor() as cur:
                await cur.execute(query, *args)
                # this row makes cur.execute result: [(1, 'hello')]
                # looks like this [{"user_id":1,"first_name":"hello"}]
                # to be able to use 'parse_obj'
                return [dict(zip([column[0] for column in cur.description], row))
                        for row in await cur.fetchall()]
        except Exception as e:
            logging.exception(e)
            throw_server_error(f'Database exception: {e}')
        finally:
            await self._connection_pool.release(con)

    async def close(self) -> None:
        if not self._connection_pool:
            try:
                await self._connection_pool.close()
                logging.info("Database pool connection closed")
            except Exception as e:
                logging.exception(e)
                throw_server_error(f'Database exception: {e}')
