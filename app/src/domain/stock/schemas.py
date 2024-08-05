from pydantic import BaseModel

from ..car.schemas import Car


class StockBase(BaseModel):
    id: int


class StockCreate(BaseModel):
    car_id: int
    quantity: int


class Stock(StockBase):
    car: Car
    quantity: int

    class Config:
        orm_mode = True
