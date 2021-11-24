from pydantic import BaseModel


class CarType(BaseModel):
    car_type_id: int
    name: str
    amount_of_seats: int
