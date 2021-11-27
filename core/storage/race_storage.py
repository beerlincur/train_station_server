from datetime import datetime
from typing import List

from core.model.order import Order
from core.model.race import RaceResponse, RaceConductorResponse
from core.model.road import Road
from core.model.road_station import RoadStationRaceResponse
from core.model.station import Station
from core.model.ticket import TicketRaceResponse, TicketConductorResponse
from core.model.train import Train
from core.model.user import User
from core.storage.sql_server import DB


class RaceStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_all_future_races(self) -> List[RaceResponse]:
        sql = 'SELECT DISTINCT race_number FROM [RoadStation] WHERE departure_time >= ?'
        race_numbers = await self.db.execute(sql, datetime.now())

        output = []
        for race_n in race_numbers:
            race_n = race_n['race_number']

            sql2 = 'SELECT rs.road_station_id as road_station_id, ' \
                   'rs.road_id as road_id, ' \
                   'r.name as road_name, ' \
                   's.station_id as station_id, ' \
                   's.name as station_name, ' \
                   't.train_id as train_id, ' \
                   't.name as train_name, ' \
                   'rs.num_in_road as num_in_road, ' \
                   'rs.arrival_time as arrival_time, ' \
                   'rs.departure_time as departure_time, ' \
                   'rs.race_number as race_number ' \
                   'FROM [RoadStation] as rs ' \
                   'JOIN [Road] AS r ON r.road_id = rs.road_id ' \
                   'JOIN [Station] AS s ON s.station_id = rs.station_id ' \
                   'JOIN [Train] AS t ON t.train_id = rs.train_id ' \
                   'WHERE race_number = ?'
            stations = await self.db.execute(sql2, race_n)

            road_stations = []
            for s in stations:
                road_stations.append(
                    RoadStationRaceResponse(
                        road_station_id=s['road_station_id'],
                        station=Station(station_id=s['station_id'], name=s['station_name']),
                        num_in_road=s['num_in_road'],
                        arrival_time=s['arrival_time'],
                        departure_time=s['departure_time'],
                    )
                )

            sql3 = 'SELECT t.ticket_id as ticket_id, ' \
                   'dep_s.name as dep_st_name, ' \
                   'dep_rs.departure_time as dep_st_time, ' \
                   'arr_s.name as arr_st_name, ' \
                   'arr_rs.arrival_time as arr_st_time, ' \
                   't.car_number as car_number, ' \
                   't.seat_number as seat_number, ' \
                   't.is_bought as is_bought, ' \
                   't.is_in_train as is_in_train ' \
                   'FROM [Ticket] as t ' \
                   'JOIN [RoadStation] as dep_rs ON dep_rs.road_station_id = t.departure_station_id ' \
                   'JOIN [RoadStation] as arr_rs ON arr_rs.road_station_id = t.arrival_station_id ' \
                   'JOIN [Station] as dep_s ON dep_s.station_id = dep_rs.station_id ' \
                   'JOIN [Station] as arr_s ON arr_s.station_id = arr_rs.station_id ' \
                   'WHERE t.race_number = ?'

            tickets = await self.db.execute(sql3, race_n)
            tickets_resp = []
            for t in tickets:
                tickets_resp.append(
                    TicketRaceResponse(
                        ticket_id=t['ticket_id'],
                        departure_station_name=t['dep_st_name'],
                        departure_station_time=t['dep_st_time'],
                        arrival_station_name=t['arr_st_name'],
                        arrival_station_time=t['arr_st_time'],
                        car_number=t['car_number'],
                        seat_number=t['seat_number'],
                        is_bought=t['is_bought'],
                        is_in_train=t['is_in_train']
                    )
                )

            output.append(
                RaceResponse(
                    race_number=race_n,
                    road=Road(road_id=stations[0]['road_id'], name=stations[0]['road_name']),
                    train=Train(train_id=stations[0]['train_id'], name=stations[0]['train_name']),
                    stations=road_stations,
                    tickets=tickets_resp
                )
            )
        return output

    async def get_races_by_road(self, road_id: int) -> List[RaceResponse]:
        sql = 'SELECT DISTINCT race_number FROM [RoadStation] WHERE departure_time >= ? AND road_id = ?'
        race_numbers = await self.db.execute(sql, datetime.now(), road_id)

        output = []
        for race_n in race_numbers:
            race_n = race_n['race_number']

            sql2 = 'SELECT rs.road_station_id as road_station_id, ' \
                   'rs.road_id as road_id, ' \
                   'r.name as road_name, ' \
                   's.station_id as station_id, ' \
                   's.name as station_name, ' \
                   't.train_id as train_id, ' \
                   't.name as train_name, ' \
                   'rs.num_in_road as num_in_road, ' \
                   'rs.arrival_time as arrival_time, ' \
                   'rs.departure_time as departure_time, ' \
                   'rs.race_number as race_number ' \
                   'FROM [RoadStation] as rs ' \
                   'JOIN [Road] AS r ON r.road_id = rs.road_id ' \
                   'JOIN [Station] AS s ON s.station_id = rs.station_id ' \
                   'JOIN [Train] AS t ON t.train_id = rs.train_id ' \
                   'WHERE race_number = ?'
            stations = await self.db.execute(sql2, race_n)

            road_stations = []
            for s in stations:
                road_stations.append(
                    RoadStationRaceResponse(
                        road_station_id=s['road_station_id'],
                        station=Station(station_id=s['station_id'], name=s['station_name']),
                        num_in_road=s['num_in_road'],
                        arrival_time=s['arrival_time'],
                        departure_time=s['departure_time'],
                    )
                )

            sql3 = 'SELECT t.ticket_id as ticket_id, ' \
                   'dep_s.name as dep_st_name, ' \
                   'dep_rs.departure_time as dep_st_time, ' \
                   'arr_s.name as arr_st_name, ' \
                   'arr_rs.arrival_time as arr_st_time, ' \
                   't.car_number as car_number, ' \
                   't.seat_number as seat_number, ' \
                   't.is_bought as is_bought, ' \
                   't.is_in_train as is_in_train ' \
                   'FROM [Ticket] as t ' \
                   'JOIN [RoadStation] as dep_rs ON dep_rs.road_station_id = t.departure_station_id ' \
                   'JOIN [RoadStation] as arr_rs ON arr_rs.road_station_id = t.arrival_station_id ' \
                   'JOIN [Station] as dep_s ON dep_s.station_id = dep_rs.station_id ' \
                   'JOIN [Station] as arr_s ON arr_s.station_id = arr_rs.station_id ' \
                   'WHERE t.race_number = ?'

            tickets = await self.db.execute(sql3, race_n)
            tickets_resp = []
            for t in tickets:
                tickets_resp.append(
                    TicketRaceResponse(
                        ticket_id=t['ticket_id'],
                        departure_station_name=t['dep_st_name'],
                        departure_station_time=t['dep_st_time'],
                        arrival_station_name=t['arr_st_name'],
                        arrival_station_time=t['arr_st_time'],
                        car_number=t['car_number'],
                        seat_number=t['seat_number'],
                        is_bought=t['is_bought'],
                        is_in_train=t['is_in_train']
                    )
                )

            output.append(
                RaceResponse(
                    race_number=race_n,
                    road=Road(road_id=stations[0]['road_id'], name=stations[0]['road_name']),
                    train=Train(train_id=stations[0]['train_id'], name=stations[0]['train_name']),
                    stations=road_stations,
                    tickets=tickets_resp
                )
            )
        return output

    async def get_races_by_conductor(self, conductor_id: int) -> List[RaceConductorResponse]:
        sql = 'SELECT DISTINCT race_number FROM [RoadStation] as rs ' \
              'JOIN [TrainCar] as tc ON tc.train_id = rs.train_id ' \
              'WHERE rs.departure_time >= ? AND tc.conductor_id = ?'
        race_numbers = await self.db.execute(sql, datetime.now(), conductor_id)

        output = []
        for race_n in race_numbers:
            race_n = race_n['race_number']

            sql2 = 'SELECT rs.road_station_id as road_station_id, ' \
                   'rs.road_id as road_id, ' \
                   'r.name as road_name, ' \
                   's.station_id as station_id, ' \
                   's.name as station_name, ' \
                   't.train_id as train_id, ' \
                   't.name as train_name, ' \
                   'rs.num_in_road as num_in_road, ' \
                   'rs.arrival_time as arrival_time, ' \
                   'rs.departure_time as departure_time, ' \
                   'rs.race_number as race_number ' \
                   'FROM [RoadStation] as rs ' \
                   'JOIN [Road] AS r ON r.road_id = rs.road_id ' \
                   'JOIN [Station] AS s ON s.station_id = rs.station_id ' \
                   'JOIN [Train] AS t ON t.train_id = rs.train_id ' \
                   'WHERE race_number = ?'
            stations = await self.db.execute(sql2, race_n)

            road_stations = []
            for s in stations:
                road_stations.append(
                    RoadStationRaceResponse(
                        road_station_id=s['road_station_id'],
                        station=Station(station_id=s['station_id'], name=s['station_name']),
                        num_in_road=s['num_in_road'],
                        arrival_time=s['arrival_time'],
                        departure_time=s['departure_time'],
                    )
                )

            sql3 = 'SELECT t.ticket_id as ticket_id, ' \
                   'dep_s.name as dep_st_name, ' \
                   'arr_s.name as arr_st_name, ' \
                   't.car_number as car_number, ' \
                   't.seat_number as seat_number, ' \
                   't.is_bought as is_bought, ' \
                   't.is_in_train as is_in_train, ' \
                   'ord.order_id as order_id, ' \
                   'ord.created_at as order_created_at, ' \
                   'ord.is_canceled as order_is_canceled, ' \
                   'u.user_id as user_id, ' \
                   'u.first_name as user_first_name, ' \
                   'u.second_name as user_second_name, ' \
                   'u.middle_name as user_middle_name, ' \
                   'u.passport as user_passport ' \
                   'FROM [Ticket] as t ' \
                   'JOIN [RoadStation] as dep_rs ON dep_rs.road_station_id = t.departure_station_id ' \
                   'JOIN [RoadStation] as arr_rs ON arr_rs.road_station_id = t.arrival_station_id ' \
                   'JOIN [Station] as dep_s ON dep_s.station_id = dep_rs.station_id ' \
                   'JOIN [Station] as arr_s ON arr_s.station_id = arr_rs.station_id ' \
                   'LEFT JOIN [Order] as ord ON ord.ticket_id = t.ticket_id ' \
                   'JOIN [User] as u ON u.user_id = ord.user_id ' \
                   'WHERE t.race_number = ?'

            tickets = await self.db.execute(sql3, race_n)
            tickets_resp = []
            for t in tickets:
                tickets_resp.append(
                    TicketConductorResponse(
                        ticket_id=t['ticket_id'],
                        departure_station_name=t['dep_st_name'],
                        arrival_station_name=t['arr_st_name'],
                        car_number=t['car_number'],
                        seat_number=t['seat_number'],
                        is_bought=t['is_bought'],
                        is_in_train=t['is_in_train'],
                        order_order_id=t['order_id'],
                        order_created_at=t['order_created_at'],
                        order_is_canceled=t['order_is_canceled'],
                        user_first_name=t['user_first_name'],
                        user_second_name=t['user_second_name'],
                        user_passport=t['user_passport']
                        )
                    )

            output.append(
                RaceConductorResponse(
                    race_number=race_n,
                    road=Road(road_id=stations[0]['road_id'], name=stations[0]['road_name']),
                    train=Train(train_id=stations[0]['train_id'], name=stations[0]['train_name']),
                    stations=road_stations,
                    tickets=tickets_resp
                )
            )
        return output

