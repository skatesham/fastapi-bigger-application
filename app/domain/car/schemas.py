from typing import List, Optional

from pydantic import BaseModel


class CarBase(BaseModel):
    id: int

    
    
class CarCreate(BaseModel):
    name: str
    year: str
    brand: str


class Car(CarBase):
    name: str
    year: str
    brand: str
   
    class Config:
        orm_mode = True
        
