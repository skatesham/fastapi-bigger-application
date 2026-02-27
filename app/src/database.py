import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

###
# Database Configuration
###

SQLALCHEMY_DATABASE_URL = "postgresql://skatesham:skatesham-github@localhost/skatesham"

engine = create_engine(os.getenv("DB_URL", SQLALCHEMY_DATABASE_URL))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass
