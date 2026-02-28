###
# Tables for clear on test - ordered to respect foreign key constraints
###

tables = (
    "sales",      # Depends on cars, buyers, sellers
    "stocks",     # Depends on cars
    "items",      # Depends on users
    "buyers",     # No dependencies
    "sellers",    # No dependencies
    "cars",       # No dependencies
    "users",      # No dependencies
)
