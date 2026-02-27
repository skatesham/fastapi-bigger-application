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
from app.src.domain.buyer import service as buyer_service
from app.src.domain.car import repository as car_repository, service as car_service
from app.src.domain.sale import service as sale_service
from app.src.domain.seller import service as seller_service
from app.src.domain.stock import service as stock_service
from app.src.domain.user import service as user_service


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
def get_buyer_service() -> buyer_service:
    return buyer_service

def get_car_repository() -> car_repository:
    return car_repository

def get_car_service() -> car_service:
    return car_service

def get_sale_service() -> sale_service:
    return sale_service

def get_seller_service() -> seller_service:
    return seller_service

def get_stock_service() -> stock_service:
    return stock_service

def get_user_service() -> user_service:
    return user_service

# Annotated Dependencies for clean injection
BuyerService = Annotated[buyer_service, Depends(get_buyer_service)]
CarRepository = Annotated[car_repository, Depends(get_car_repository)]
CarService = Annotated[car_service, Depends(get_car_service)]
SaleService = Annotated[sale_service, Depends(get_sale_service)]
SellerService = Annotated[seller_service, Depends(get_seller_service)]
StockService = Annotated[stock_service, Depends(get_stock_service)]
UserService = Annotated[user_service, Depends(get_user_service)]

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
