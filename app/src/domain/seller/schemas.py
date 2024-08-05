from pydantic import BaseModel


class SellerBase(BaseModel):
    id: int


class SellerCreate(BaseModel):
    name: str
    cpf: str
    phone: str


class Seller(SellerBase):
    name: str
    cpf: str
    phone: str

    class Config:
        orm_mode = True
