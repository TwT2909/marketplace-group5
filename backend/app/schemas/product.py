from datetime import datetime
from pydantic import BaseModel, field_validator


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    quantity: int

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float) -> float:
        if v <= 0:
            raise ValueError("Цена должна быть больше 0")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_non_negative(cls, v: int) -> int:
        if v < 0:
            raise ValueError("Количество не может быть отрицательным")
        return v


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v: float | None) -> float | None:
        if v is not None and v <= 0:
            raise ValueError("Цена должна быть больше 0")
        return v

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_non_negative(cls, v: int | None) -> int | None:
        if v is not None and v < 0:
            raise ValueError("Количество не может быть отрицательным")
        return v


class ProductOut(BaseModel):
    id: int
    owner_id: int
    name: str
    description: str | None
    price: float
    quantity: int
    image_url: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
