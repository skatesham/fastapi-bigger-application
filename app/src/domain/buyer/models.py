from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from ...database import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    address_cep = Column(String)
    address_public_place = Column(String)
    address_city = Column(String)
    address_district = Column(String)
    address_state = Column(String)
    
    sale = relationship("Sale", back_populates="buyer")
    
