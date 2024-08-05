import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

###
# Database Configuration
###

SQLALCHEMY_DATABASE_URL = "postgresql://skatesham:skatesham-github@localhost/skatesham"

engine = create_engine(
    os.getenv("DB_URL", SQLALCHEMY_DATABASE_URL)
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
