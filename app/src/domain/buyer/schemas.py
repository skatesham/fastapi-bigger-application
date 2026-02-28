from pydantic import BaseModel, ConfigDict
from typing import Optional


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


class BuyerUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[Address] = None
    phone: Optional[str] = None


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
    address_cep: str
    address_public_place: str
    address_city: str
    address_district: str
    address_state: str

    model_config = ConfigDict(from_attributes=True)
