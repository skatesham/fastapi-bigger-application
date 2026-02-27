from pydantic import BaseModel
from typing import Optional
from app.src.core.conversion import convert_model_to_schema, convert_many_models_to_schemas


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
    address: Address

    class Config:
        from_attributes = True
    
    @classmethod
    def from_model(cls, db_model):
        """Convert SQLAlchemy model to Pydantic schema directly"""
        return convert_model_to_schema(
            db_model=db_model,
            schema_class=cls,
            nested_objects={'address': Address}
        )
    
    @classmethod
    def from_models(cls, db_models):
        """Convert list of SQLAlchemy models to Pydantic schemas directly"""
        return convert_many_models_to_schemas(
            db_models=db_models,
            schema_class=cls,
            nested_objects={'address': Address}
        )
