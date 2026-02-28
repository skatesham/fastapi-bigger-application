"""
Dependencies for API endpoints using FastAPI Annotated patterns
Centralized dependency injection for clean architecture
"""

from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.src.core.database import SessionLocal
from app.src.core.security import get_current_user
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


# Service Dependencies - Direct singleton imports
Database = Annotated[Session, Depends(get_db)]

# Direct dependencies using singleton instances
BuyerService = Annotated[BuyerServiceClass, Depends(lambda: buyer_service)]
CarRepository = Annotated[CarRepositoryClass, Depends(lambda: car_repository)]
CarService = Annotated[CarServiceClass, Depends(lambda: car_service)]
SaleService = Annotated[SaleServiceClass, Depends(lambda: sale_service)]
SellerService = Annotated[SellerServiceClass, Depends(lambda: seller_service)]
StockService = Annotated[StockServiceClass, Depends(lambda: stock_service)]
UserService = Annotated[UserServiceClass, Depends(lambda: user_service)]

# Security Annotated Dependencies
CurrentUser = Annotated[dict, Depends(get_current_user)]


# Common Dependencies mapping
CommonDependencies = {
    "db": Database,
    "buyer_service": BuyerService,
    "car_repository": CarRepository,
    "car_service": CarService,
    "sale_service": SaleService,
    "seller_service": SellerService,
    "stock_service": StockService,
    "user_service": UserService,
    "current_user": CurrentUser,
}
