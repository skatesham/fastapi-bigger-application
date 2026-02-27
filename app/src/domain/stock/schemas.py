from pydantic import BaseModel
from ..car.schemas import Car
from app.src.core.conversion import convert_model_to_schema, convert_many_models_to_schemas


class StockBase(BaseModel):
    id: int


class StockCreate(BaseModel):
    car_id: int
    quantity: int


class Stock(StockBase):
    car: Car
    quantity: int

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
