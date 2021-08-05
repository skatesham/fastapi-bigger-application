from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ...src.database import Base

from ...src.dependencies import get_db


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def configure_test_database(app):
    app.dependency_overrides[get_db] = override_get_db


def truncate_tables(data):
    with engine.connect() as con:
        
        IGNORE_CONSTRAINTS = """PRAGMA ignore_check_constraints = 0"""
        DISABLE_IGNORE_CONSTRAINTS = """PRAGMA ignore_check_constraints = 1"""

        statement = """DELETE FROM {table:s}"""

        con.execute(IGNORE_CONSTRAINTS)
        for line in data:
            con.execute(statement.format(table = line))
        con.execute(DISABLE_IGNORE_CONSTRAINTS)
    
    