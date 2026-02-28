from pydantic import BaseModel, ConfigDict
from typing import Optional


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

    model_config = ConfigDict(from_attributes=True)
