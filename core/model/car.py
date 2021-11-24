from pydantic import BaseModel


class Car(BaseModel):
    car_id: int
    type_id: int
    number: int
