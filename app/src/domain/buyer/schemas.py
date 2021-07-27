from typing import Optional
from app.src.domain.sale.models import Sale
from pydantic import BaseModel
 
class Address(BaseModel):
    cep: str
    public_place: str
    city: str
    district: str
    state: str
        

class BuyerBase(BaseModel):
    id: int
    
    
class BuyerCreate(BaseModel):
    name: str
    address: Address
    phone: str
    
    
class BuyerSimpleResponse(BaseModel):
    id: int
    name: str
    phone: str
    address_cep: str
    address_public_place: str
    address_city: str
    address_district: str
    address_state: str

    

class Buyer(BuyerBase):
    name: str
    phone: str
    address: Address
   
    class Config:
        orm_mode = True
        
