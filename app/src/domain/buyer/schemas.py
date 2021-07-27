from pydantic import BaseModel
 
class Address(BaseModel):
    cep: str
    public_place: str
    city: str
    district: str
    state: str
        

class BuyerBase(BaseModel):
    id: int
    address: Address
    
    
class BuyerCreate(BaseModel):
    name: str
    address: Address
    phone: str


class Buyer(BuyerBase):
    name: str
    phone: str
    address: Address
   
    class Config:
        orm_mode = True
        
