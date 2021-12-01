from typing import List

from core.model.car import CarResponse
from core.model.car_type import CarType
from core.model.train import Train, TrainResponse
from core.storage.sql_server import DB


class TrainStorage:
    def __init__(self, db: DB) -> None:
        self.db = db

    async def get_by_id(self, train_id: int) -> Train:
        sql = 'SELECT * from [Train] WHERE train_id = ?'
        row = await self.db.execute(sql, train_id)
        return Train.parse_obj(row[0])

    async def get_all(self) -> List[TrainResponse]:
        sql = 'SELECT train_id, name from [Train] ORDER BY train_id'
        rows = await self.db.execute(sql)
        output = []
        for row in rows:
            sql2 = 'SELECT c.car_id as car_id, ' \
                   'c.number as car_number, ' \
                   'ct.car_type_id as type_id, ' \
                   'ct.name as type_name, ' \
                   'ct.amount_of_seats as am_of_seats FROM [Car] as c ' \
                   'JOIN [CarType] as ct ON ct.car_type_id = c.type_id ' \
                   'WHERE c.car_id IN (SELECT car_id FROM [TrainCar] WHERE train_id = ?)'
            rows_cars = await self.db.execute(sql2, row['train_id'])
            cars = []
            for car in rows_cars:
                cars.append(
                    CarResponse(
                        car_id=car['car_id'],
                        type=CarType(
                            car_type_id=car['type_id'],
                            name=car['type_name'],
                            amount_of_seats=car['am_of_seats']
                        ),
                        number=car['car_number']
                    )
                )
            output.append(
                TrainResponse(
                    train_id=row['train_id'],
                    name=row['name'],
                    cars=cars
                )
            )
        return output

    async def create(self, name) -> None:
        sql = 'INSERT INTO [Train] VALUES (?)'
        row = await self.db.execute(sql, name)
