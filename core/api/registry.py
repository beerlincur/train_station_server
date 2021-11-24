import datetime
import os

from core.storage import sql_server
from core.storage.order_storage import OrderStorage
from core.storage.ping_storage import PingStorage
from core.storage.race_storage import RaceStorage
from core.storage.road_station_storage import RoadStationStorage
from core.storage.road_storage import RoadStorage
from core.storage.station_storage import StationStorage
from core.storage.ticket_storage import TicketStorage
from core.storage.train_storage import TrainStorage
from core.storage.user_storage import UserStorage

server_started = datetime.datetime.now()
VERSION = os.getenv('VERSION', '1')

db: sql_server.DB = sql_server.get_database()

ping_storage = PingStorage(db)
user_storage = UserStorage(db)
ticket_storage = TicketStorage(db)
road_storage = RoadStorage(db)
road_station_storage = RoadStationStorage(db)
station_storage = StationStorage(db)
train_storage = TrainStorage(db)
race_storage = RaceStorage(db)
order_storage = OrderStorage(db)

