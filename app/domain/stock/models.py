from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from ...database import Base


class Stock(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer)
    car_id = Column(Integer, ForeignKey("cars.id"), unique=True)
    
    car = relationship("Car", back_populates="stock")
    
