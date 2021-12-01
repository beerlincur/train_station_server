from pydantic import BaseModel


class Train(BaseModel):
    train_id: int
    name: str

class TrainCreateRequest(BaseModel):
    name: str

