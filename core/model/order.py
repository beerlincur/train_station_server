from datetime import datetime

from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    user_id: int
    ticket_id: int
    created_at: datetime
    is_canceled: bool
