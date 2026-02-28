from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.src.core.database import Base
from app.src.api.deps import get_db

## Configure SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Method for override database default configuration"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


def configure_test_database(app):
    """Override default database for test embedded database"""

    Base.metadata.create_all(bind=engine)

    app.dependency_overrides[get_db] = override_get_db


def truncate_tables(tables):
    """Truncate rows of all input tables"""

    with engine.connect() as con:
        # Use text() for proper SQL execution
        from sqlalchemy import text
        
        IGNORE_CONSTRAINTS = text("PRAGMA ignore_check_constraints = 0")
        DISABLE_IGNORE_CONSTRAINTS = text("PRAGMA ignore_check_constraints = 1")

        con.execute(IGNORE_CONSTRAINTS)
        for table in tables:
            DELETE_STATEMENT = text(f"DELETE FROM {table}")
            con.execute(DELETE_STATEMENT)
        con.execute(DISABLE_IGNORE_CONSTRAINTS)
        con.commit()
