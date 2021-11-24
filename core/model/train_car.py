from pydantic import BaseModel


class TrainCar(BaseModel):
    train_id: int
    car_id: int
    conductor_id: int
