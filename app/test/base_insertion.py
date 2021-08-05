from sqlalchemy.sql import text

from .config import database_test_config


engine = database_test_config.engine


def insert_into_cars(input):
    """ Insert row into table cars for test mass """
    with engine.connect() as con:

        data = (input, )

        statement = text(
            """INSERT INTO cars(id, name, year, brand) VALUES(:id, :name, :year, :brand)""")

        for line in data:
            con.execute(statement, **line)


def insert_into_sellers(input):
    with engine.connect() as con:

        data = (input, )

        statement = text(
            """INSERT INTO sellers(id, name, cpf, phone) VALUES(:id, :name, :cpf, :phone)""")

        for line in data:
            con.execute(statement, **line)


def insert_into_buyers(input):
    with engine.connect() as con:

        data = (
            {
                "id": input["id"],
                "name":input["name"],
                "phone": input["phone"],
                "address_cep": input["address"]["cep"],
                "address_public_place": input["address"]["public_place"],
                "address_district": input["address"]["district"],
                "address_city": input["address"]["city"],
                "address_state": input["address"]["state"]
            },
        )


        statement = text("""INSERT INTO buyers( 
            id, name, phone, address_cep, address_public_place, 
            address_district, address_city, address_state) 
            VALUES(:id, :name, :phone, :address_cep, :address_public_place,
            :address_district, :address_city, :address_state)""")

        for line in data:
            con.execute(statement, **line)
            

def insert_into_stocks(input):
    """ Insert row into table cars for test mass """
    with engine.connect() as con:

        data = (input, )

        statement = text(
            """INSERT INTO stocks(id, car_id, quantity) VALUES(:id, :car_id, :quantity)""")

        for line in data:
            con.execute(statement, **line)


def insert_into_sales(input):
    """ Insert row into table cars for test mass """
    with engine.connect() as con:

        data = (input, )

        statement = text(
            """INSERT INTO sales(id, car_id, buyer_id, seller_id, created_at) VALUES(:id, :car_id, :buyer_id, :seller_id, :created_at)""")

        for line in data:
            con.execute(statement, **line)

