from pydantic import BaseModel, ConfigDict
from typing import Optional
from ..car.schemas import Car


class StockBase(BaseModel):
    id: int


class StockCreate(BaseModel):
    car_id: int
    quantity: int


class StockUpdate(BaseModel):
    car_id: Optional[int] = None
    quantity: Optional[int] = None


class Stock(StockBase):
    car: Car
    quantity: int

    model_config = ConfigDict(from_attributes=True)
