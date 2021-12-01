from typing import List

from pydantic import BaseModel

from core.model.car import CarResponse


class Train(BaseModel):
    train_id: int
    name: str


class TrainCreateRequest(BaseModel):
    name: str


class TrainResponse(BaseModel):
    train_id: int
    name: str
    cars: List[CarResponse]


