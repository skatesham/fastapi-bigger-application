"""
Dependencies for API endpoints using FastAPI Annotated patterns
Centralized dependency injection for clean architecture
"""

from typing import Annotated, List, Optional
from functools import lru_cache

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from jose import jwt

from app.src.database import SessionLocal
from app.src.config import SECRET_KEY, ALGORITHM
from app.src.domain.buyer import service as buyer_service
from app.src.domain.car import repository as car_repository, service as car_service
from app.src.domain.sale import service as sale_service
from app.src.domain.seller import service as seller_service
from app.src.domain.stock import service as stock_service
from app.src.domain.user import service as user_service
from app.src.api.converters import (
    buyer_converter, car_converter, sale_converter, 
    seller_converter, stock_converter
)


# Database Dependency
def get_db() -> Session:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Security Dependencies
# Using config values from app.src.config


def decode(token: str) -> dict:
    """Decode JWT token"""
    stripped_token = token.replace("Bearer ", "")
    return jwt.decode(stripped_token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_token_header(x_token: str = Header(...)) -> dict:
    """Example header validation dependency"""
    payload = decode(x_token)
    username: str = payload.get("email")
    if username is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return payload


async def get_query_token(token: str) -> str:
    """Example query token validation"""
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    return token


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

def get_buyer_converter() -> buyer_converter:
    return buyer_converter

def get_car_converter() -> car_converter:
    return car_converter

def get_sale_converter() -> sale_converter:
    return sale_converter

def get_seller_converter() -> seller_converter:
    return seller_converter

def get_stock_converter() -> stock_converter:
    return stock_converter

# Annotated Dependencies for clean injection
BuyerService = Annotated[buyer_service, Depends(get_buyer_service)]
CarRepository = Annotated[car_repository, Depends(get_car_repository)]
CarService = Annotated[car_service, Depends(get_car_service)]
SaleService = Annotated[sale_service, Depends(get_sale_service)]
SellerService = Annotated[seller_service, Depends(get_seller_service)]
StockService = Annotated[stock_service, Depends(get_stock_service)]
UserService = Annotated[user_service, Depends(get_user_service)]
BuyerConverter = Annotated[buyer_converter, Depends(get_buyer_converter)]
CarConverter = Annotated[car_converter, Depends(get_car_converter)]
SaleConverter = Annotated[sale_converter, Depends(get_sale_converter)]
SellerConverter = Annotated[seller_converter, Depends(get_seller_converter)]
StockConverter = Annotated[stock_converter, Depends(get_stock_converter)]

# Security Annotated Dependencies
TokenHeader = Annotated[dict, Depends(get_token_header)]
QueryToken = Annotated[str, Depends(get_query_token)]


# Common Dependencies mapping
CommonDependencies = {
    "db": Database,
    "buyer_service": BuyerService,
    "buyer_converter": BuyerConverter,
    "car_repository": CarRepository,
    "car_service": CarService,
    "car_converter": CarConverter,
    "sale_service": SaleService,
    "sale_converter": SaleConverter,
    "seller_service": SellerService,
    "seller_converter": SellerConverter,
    "stock_converter": StockConverter,
    "stock_service": StockService,
    "user_service": UserService,
    "token_header": TokenHeader,
    "query_token": QueryToken,
}


@lru_cache()
def get_dependency(name: str):
    """Cached dependency getter for performance"""
    return CommonDependencies.get(name)
