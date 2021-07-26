from typing import List, Optional

from pydantic import BaseModel


class BuyerBase(BaseModel):
    id: int
    
    
class BuyerCreate(BaseModel):
    name: str
    phone: str


class Buyer(BuyerBase):
    name: str
    phone: str
   
    class Config:
        orm_mode = True
        
