from datetime import datetime
from sqlalchemy import Column, ForeignKey, Integer, DateTime
from sqlalchemy.orm import relationship

from ...database import Base


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    car_id = Column(Integer, ForeignKey("cars.id"))
    buyer_id = Column(Integer, ForeignKey("buyers.id"))
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    car = relationship("Car", back_populates="sale")
    buyer = relationship("Buyer", back_populates="sale")
    seller = relationship("Seller", back_populates="sale")
    
