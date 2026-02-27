from pydantic import BaseModel
from app.src.core.conversion import convert_model_to_schema, convert_many_models_to_schemas


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
        from_attributes = True
    
    @classmethod
    def from_model(cls, db_model):
        """Convert SQLAlchemy model to Pydantic schema directly"""
        return convert_model_to_schema(db_model=db_model, schema_class=cls)
    
    @classmethod
    def from_models(cls, db_models):
        """Convert list of SQLAlchemy models to Pydantic schemas directly"""
        return convert_many_models_to_schemas(db_models=db_models, schema_class=cls)
