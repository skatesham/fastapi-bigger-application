from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..database import Base

from ..dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

def configure_test_database(app):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    app.dependency_overrides[get_db] = override_get_db


def insert_into_seller():
    from sqlalchemy.sql import text
    with engine.connect() as con:

        data = ( { "id": 1, "name": "João da Silva", "cpf": "69285717640", "phone": "1299871234" },
                { "id": 2, "name": "Maria de Souza", "cpf": "42843444128", "phone": "1299874321" },
        )

        statement = text("""INSERT INTO sellers(id, name, cpf, phone) VALUES(:id, :name, :cpf, :phone)""")

        for line in data:
            con.execute(statement, **line)