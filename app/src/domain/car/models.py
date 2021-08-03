from sqlalchemy import Column, Integer, String, UniqueConstraint

from sqlalchemy.orm import relationship

from ...database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    year = Column(Integer, index=True)
    brand = Column(String, index=True)
    
    stock = relationship("Stock", back_populates="car")
    sale = relationship("Sale", back_populates="car")
    UniqueConstraint('year', 'name', 'brand', name='cars_year_name_brand_uk_idx1')

