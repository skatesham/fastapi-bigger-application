"""
Dependencies for API endpoints using FastAPI Annotated patterns
Centralized dependency injection for clean architecture
"""

from typing import Annotated, List, Optional
from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.core.database import SessionLocal
from app.src.core.config import SECRET_KEY, ALGORITHM
from app.src.core.security import get_token_header, get_query_token, TokenHeader, QueryToken
# Import the actual classes for type hints
from app.src.domain.buyer.service import BuyerService as BuyerServiceClass
from app.src.domain.car.repository import CarRepository as CarRepositoryClass
from app.src.domain.car.service import CarService as CarServiceClass
from app.src.domain.sale.service import SaleService as SaleServiceClass
from app.src.domain.seller.service import SellerService as SellerServiceClass
from app.src.domain.stock.service import StockService as StockServiceClass
from app.src.domain.user.service import UserService as UserServiceClass

# Import singleton instances
from app.src.domain.buyer.service import buyer_service
from app.src.domain.car.repository import car_repository
from app.src.domain.car.service import car_service
from app.src.domain.sale.service import sale_service
from app.src.domain.seller.service import seller_service
from app.src.domain.stock.service import stock_service
from app.src.domain.user.service import user_service


# Database Dependency
def get_db() -> Session:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Security Dependencies
# Using core.security module


# Service Dependencies - Using functions directly since no classes exist yet
Database = Annotated[Session, Depends(get_db)]

# Function-based dependencies for services
def get_buyer_service() -> BuyerServiceClass:
    return buyer_service

def get_car_repository() -> CarRepositoryClass:
    return car_repository

def get_car_service() -> CarServiceClass:
    return car_service

def get_sale_service() -> SaleServiceClass:
    return sale_service

def get_seller_service() -> SellerServiceClass:
    return seller_service

def get_stock_service() -> StockServiceClass:
    return stock_service

def get_user_service() -> UserServiceClass:
    return user_service

# Annotated Dependencies for clean injection
BuyerService = Annotated[BuyerServiceClass, Depends(get_buyer_service)]
CarRepository = Annotated[CarRepositoryClass, Depends(get_car_repository)]
CarService = Annotated[CarServiceClass, Depends(get_car_service)]
SaleService = Annotated[SaleServiceClass, Depends(get_sale_service)]
SellerService = Annotated[SellerServiceClass, Depends(get_seller_service)]
StockService = Annotated[StockServiceClass, Depends(get_stock_service)]
UserService = Annotated[UserServiceClass, Depends(get_user_service)]

# Security Annotated Dependencies
TokenHeader = Annotated[dict, Depends(get_token_header)]
QueryToken = Annotated[str, Depends(get_query_token)]


# Common Dependencies mapping
CommonDependencies = {
    "db": Database,
    "buyer_service": BuyerService,
    "car_repository": CarRepository,
    "car_service": CarService,
    "sale_service": SaleService,
    "seller_service": SellerService,
    "stock_service": StockService,
    "stock_service": StockService,
    "user_service": UserService,
    "token_header": TokenHeader,
    "query_token": QueryToken,
}


@lru_cache()
def get_dependency(name: str):
    """Cached dependency getter for performance"""
    return CommonDependencies.get(name)
