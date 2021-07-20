from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from ...database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    year = Column(Integer, index=True)
    brand = Column(String, index=True)
    
    stock = relationship("Stock", back_populates="car")
    
