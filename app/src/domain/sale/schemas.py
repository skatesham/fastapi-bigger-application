from datetime import datetime
from pydantic import BaseModel

from ..car.schemas import Car
from ..buyer.schemas import Buyer
from ..seller.schemas import Seller


class SaleBase(BaseModel):
    id: int
    
    
class SaleCreate(BaseModel):
    car_id: int
    seller_id: int
    buyer_id: int
    
class SaleCreateResponse(SaleCreate):
    id: int

class Sale(SaleBase):
    car: Car
    buyer: Buyer
    seller: Seller
    created_at: datetime
    
    class Config:
        orm_mode = True
        
