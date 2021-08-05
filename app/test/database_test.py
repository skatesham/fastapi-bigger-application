from .config import database_test_config

from .database_tables import tables


###
# Suport test database dependencies
###

def configure_test_database(app):
    ''' Configure test database '''
    database_test_config.configure_test_database(app)
    

def clear_database():
    ''' Clear test database '''
    database_test_config.truncate_tables(tables)

