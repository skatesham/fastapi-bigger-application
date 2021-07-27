from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from ..src.database import Base

from ..src.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)


def configure_test_database(app):
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    
    app.dependency_overrides[get_db] = override_get_db    
    

def insert_into_cars():
    with engine.connect() as con:

        data = ( { "id": 1, "name": "Galardo", "year": "1999", "brand": "lamborghini" },
                { "id": 2, "name": "CX40", "year": "2021", "brand": "Volvo" },
        )

        statement = text("""INSERT INTO cars(id, name, year, brand) VALUES(:id, :name, :year, :brand)""")

        for line in data:
            con.execute(statement, **line)


def insert_into_sellers():
    with engine.connect() as con:

        data = ( { "id": 1, "name": "João da Silva", "cpf": "69285717640", "phone": "1299871234" },
                { "id": 2, "name": "Maria de Souza", "cpf": "42843444128", "phone": "1299874321" },
        )

        statement = text("""INSERT INTO sellers(id, name, cpf, phone) VALUES(:id, :name, :cpf, :phone)""")

        for line in data:
            con.execute(statement, **line)
            
def insert_into_buyers():
    with engine.connect() as con:

        data = ( 
                { 
                    "id": 1,
                    "name": "Bruce Lee",
                    "phone": "1299871234",
                    "address_cep": "73770-000",
                    "address_public_place": "Muro Preto",
                    "address_district": "Cidade Baixa",
                    "address_city": "Alto Paraíso de Goias",
                    "address_state": "Goias"
                },
                { 
                    "id": 2,
                    "name": "Bruce Willis",
                    "phone": "1299874321",
                    "address_cep": "12209-000",
                    "address_public_place": "Prédio Vermelho",
                    "address_district": "Centro",
                    "address_city": "São José dos Campos",
                    "address_state": "São Paulo"
                  }
        )

        statement = text("""INSERT INTO buyers( 
            id, name, phone, address_cep, address_public_place, 
            address_district, address_city, address_state) 
            VALUES(:id, :name, :phone, :address_cep, :address_public_place,
            :address_district, :address_city, :address_state)""")

        for line in data:
            con.execute(statement, **line)     

