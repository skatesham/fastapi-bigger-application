from typing import List

from starlette.config import Config
from starlette.datastructures import CommaSeparatedStrings

###
# Properties configurations
###

API_PREFIX = "/api"

JWT_TOKEN_PREFIX = "Authorization"

config = Config(".env")

ROUTE_PREFIX_V1 = "/v1"

ALLOWED_HOSTS: List[str] = config(
    "ALLOWED_HOSTS",
    cast=CommaSeparatedStrings,
    default="",
)

# Security Configuration
SECRET_KEY = config("SECRET_KEY", default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
ALGORITHM = config("ALGORITHM", default="HS256")

# Database Configuration
DATABASE_URL = config("DATABASE_URL", default="postgresql://skatesham:skatesham-github@localhost/skatesham")
