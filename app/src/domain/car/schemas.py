from pydantic import BaseModel


class CarBase(BaseModel):
    id: int


class CarCreate(BaseModel):
    name: str
    year: int
    brand: str


class Car(CarBase):
    name: str
    year: int
    brand: str

    class Config:
        orm_mode = True
