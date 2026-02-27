from pydantic import BaseModel
from typing import Optional
from app.src.core.conversion import convert_model_to_schema, convert_many_models_to_schemas


class CarBase(BaseModel):
    id: int


class CarCreate(BaseModel):
    name: str
    year: int
    brand: str


class CarUpdate(BaseModel):
    name: Optional[str] = None
    year: Optional[int] = None
    brand: Optional[str] = None


class Car(CarBase):
    name: str
    year: int
    brand: str

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
