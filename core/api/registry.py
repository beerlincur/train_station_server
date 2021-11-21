import datetime
import os

from core.storage import sql_server
from core.storage.ping_storage import PingStorage
from core.storage.user_storage import UserStorage

server_started = datetime.datetime.now()
VERSION = os.getenv('VERSION', '1')

db: sql_server.DB = sql_server.get_database()

ping_storage = PingStorage(db)
user_storage = UserStorage(db)

