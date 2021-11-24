from datetime import datetime

from pydantic import BaseModel

from core.model.ticket import TicketResponse


class Order(BaseModel):
    order_id: int
    user_id: int
    ticket_id: int
    created_at: datetime
    is_canceled: bool


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    ticket: TicketResponse
    created_at: datetime
    is_canceled: bool


class OrderCreateRequest(BaseModel):
    ticket_id: int
