from sqlalchemy import Column, Integer, String

from ...database import Base


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    cpf = Column(String, index=True)
    phone = Column(String)
    
