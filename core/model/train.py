from pydantic import BaseModel


class Train(BaseModel):
    train_id: int
    name: str
