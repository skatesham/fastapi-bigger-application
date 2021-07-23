from sqlalchemy import Column, Integer, String

from sqlalchemy.orm import relationship

from ...database import Base


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    phone = Column(String)
    
    sale = relationship("Sale", back_populates="buyer")
    
