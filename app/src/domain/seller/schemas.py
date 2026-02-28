from pydantic import BaseModel, ConfigDict
from typing import Optional


class SellerBase(BaseModel):
    id: int


class SellerCreate(BaseModel):
    name: str
    cpf: str
    phone: str


class SellerUpdate(BaseModel):
    name: Optional[str] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None


class Seller(SellerBase):
    name: str
    cpf: str
    phone: str

    model_config = ConfigDict(from_attributes=True)
