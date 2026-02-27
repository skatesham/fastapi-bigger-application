from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from ..buyer.schemas import Buyer
from ..car.schemas import Car
from ..seller.schemas import Seller
from app.src.core.conversion import convert_model_to_schema, convert_many_models_to_schemas


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

    class Config:
        from_attributes = True
    
    @classmethod
    def from_model(cls, db_model):
        """Convert SQLAlchemy model to Pydantic schema directly"""
        return convert_model_to_schema(db_model=db_model, schema_class=cls)
    
    @classmethod
    def from_models(cls, db_models):
        """Convert list of SQLAlchemy models to Pydantic schemas directly"""
        return convert_many_models_to_schemas(db_models=db_models, schema_class=cls)
