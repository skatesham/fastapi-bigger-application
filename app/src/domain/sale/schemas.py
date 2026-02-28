from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from ..buyer.schemas import Buyer
from ..car.schemas import Car
from ..seller.schemas import Seller


class SaleBase(BaseModel):
    id: int


class SaleCreate(BaseModel):
    car_id: int
    seller_id: int
    buyer_id: int


class SaleUpdate(BaseModel):
    car_id: Optional[int] = None
    seller_id: Optional[int] = None
    buyer_id: Optional[int] = None


class SaleCreateResponse(SaleCreate):
    id: int


class Sale(SaleBase):
    car: Car
    buyer: Buyer
    seller: Seller
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
