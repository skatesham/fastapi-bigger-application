from . import database_test_config
from .database_tables import tables

def configure_test_database(app):
    database_test_config.configure_test_database(app)


def clear_database():
    database_test_config.truncate_tables(tables)

