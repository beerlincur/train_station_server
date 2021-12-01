from pydantic import BaseModel

from core.model.car_type import CarType


class Car(BaseModel):
    car_id: int
    type_id: int
    number: int


class CarResponse(BaseModel):
    car_id: int
    type: CarType
    number: int
