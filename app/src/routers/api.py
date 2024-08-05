from fastapi import APIRouter

from . import items, users, cars, stocks, sellers, buyers, sales, auth
from ..config import ROUTE_PREFIX_V1

router = APIRouter()


def include_api_routes():
    ''' Include to router all api rest routes with version prefix '''
    router.include_router(auth.router)
    router.include_router(users.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(items.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(cars.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(stocks.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(sellers.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(buyers.router, prefix=ROUTE_PREFIX_V1)
    router.include_router(sales.router, prefix=ROUTE_PREFIX_V1)


include_api_routes()
