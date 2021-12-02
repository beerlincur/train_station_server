from datetime import datetime
from typing import List

from core.model.road_station import RoadStation, RoadStationTicketResponse, RoadStationRaceResponse
from core.model.station import Station
from core.storage.sql_server import DB
from core.utils.utils import throw_server_error


class RoadStationStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, road_station_id: int) -> RoadStation:
        sql = 'SELECT * from [RoadStation] WHERE road_station_id = ?'
        row = await self.db.execute(sql, road_station_id)
        return RoadStation.parse_obj(row[0])

    async def get_between_ids(self, departure_rs_id: int, arrival_rs_id: int) -> List[RoadStationTicketResponse]:
        sql = 'SELECT s.station_id, s.name, rs.departure_time, rs.arrival_time FROM [RoadStation] as rs ' \
              'JOIN [Station] as s ON s.station_id = rs.station_id ' \
              'WHERE rs.road_station_id >= ? AND rs.road_station_id <= ? ' \
              'ORDER BY rs.road_station_id'
        rows = await self.db.execute(sql, departure_rs_id, arrival_rs_id)
        output = []
        for row in rows:
            output.append(RoadStationTicketResponse.parse_obj(row))
        return output

    async def get_by_race(self, race_number: int) -> List[RoadStationRaceResponse]:
        sql = 'SELECT rs.road_station_id, ' \
              's.station_id, ' \
              's.name, ' \
              'rs.num_in_road, ' \
              'rs.departure_time, ' \
              'rs.arrival_time FROM [RoadStation] as rs ' \
              'JOIN [Station] as s ON s.station_id = rs.station_id ' \
              'WHERE rs.race_number = ? ' \
              'ORDER BY rs.road_station_id'
        rows = await self.db.execute(sql, race_number)
        output = []
        for row in rows:
            output.append(
                RoadStationRaceResponse(
                    road_station_id=row['road_station_id'],
                    station=Station(station_id=row['station_id'], name=row['name']),
                    num_in_road=row['num_in_road'],
                    arrival_time=row['arrival_time'],
                    departure_time=row['departure_time'],
                )
            )
        return output

    async def create(self,
                     road_id: int,
                     station_id: int,
                     train_id: int,
                     num_in_road: int,
                     arrival_time: datetime,
                     departure_time: datetime,
                     race_number: int) -> None:
        sql = 'INSERT INTO [RoadStation] (road_id,' \
              'station_id,' \
              'train_id,' \
              'num_in_road,' \
              'arrival_time,' \
              'departure_time,' \
              'race_number) VALUES (?, ?, ?, ?, ?, ?, ?)'
        row = await self.db.execute(sql,
                                    road_id,
                                    station_id,
                                    train_id,
                                    num_in_road,
                                    arrival_time,
                                    departure_time,
                                    race_number)
        if not row:
            throw_server_error("Невозможно добавить road station")
