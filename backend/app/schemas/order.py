from datetime import datetime
from pydantic import BaseModel


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    items: list[OrderItemCreate]


class OrderItemOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    price_at_order: float

    model_config = {"from_attributes": True}


class OrderOut(BaseModel):
    id: int
    buyer_id: int
    status: str
    created_at: datetime
    items: list[OrderItemOut]

    model_config = {"from_attributes": True}
