from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from ...database import Base


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cpf = Column(String, index=True)
    phone = Column(String)
    
    sale = relationship("Sale", back_populates="seller")
    
