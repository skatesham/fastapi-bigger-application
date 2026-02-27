from typing import List

from fastapi import APIRouter, HTTPException

from app.resources.strings import (
    BUYER_DOES_NOT_EXIST_ERROR,
    CAR_DOES_NOT_EXIST_ERROR,
    SALES_DOES_NOT_EXIST_ERROR,
    SELLER_DOES_NOT_EXIST_ERROR,
    STOCK_DOES_NOT_EXIST_ERROR,
)
from app.src.api.deps import (
    Database,
    BuyerService,
    CarRepository,
    SaleService,
    SellerService,
    StockService,
)
from app.src.domain.sale import schemas

router = APIRouter()


@router.post("/", response_model=schemas.Sale, status_code=201)
def create_sale(
    sale: schemas.SaleCreate,
    db: Database,
    buyer_service: BuyerService,
    car_repository: CarRepository,
    sale_service: SaleService,
    seller_service: SellerService,
    stock_service: StockService,
):
    """Create new sale using dependency injection"""
    errors = []

    if car_repository.get_car(db, car_id=sale.car_id) is None:
        errors.append(CAR_DOES_NOT_EXIST_ERROR)
    if buyer_service.get_buyer(db, buyer_id=sale.buyer_id) is None:
        errors.append(BUYER_DOES_NOT_EXIST_ERROR)
    if seller_service.get_seller(db, seller_id=sale.seller_id) is None:
        errors.append(SELLER_DOES_NOT_EXIST_ERROR)
    if stock_service.get_stock_by_car(db, car_id=sale.car_id) is None:
        errors.append(STOCK_DOES_NOT_EXIST_ERROR)
    if len(errors) > 0:
        raise HTTPException(status_code=404, detail=", ".join(errors))

    stock_service.buy_car_from_stock(db, car_id=sale.car_id, quantity=1)
    db_sale = sale_service.create_sale(db=db, sale=sale)
    return schemas.Sale.from_model(db_sale)


@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(
    sale_id: int,
    db: Database,
    sale_service: SaleService,
):
    """Get sale by ID using dependency injection"""
    db_sale = sale_service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)
    return schemas.Sale.from_model(db_sale)


@router.get("/", response_model=List[schemas.Sale])
def read_sales(
    db: Database,
    sale_service: SaleService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all sales with pagination using dependency injection"""
    db_sales = sale_service.get_sales(db, skip=skip, limit=limit)
    return schemas.Sale.from_models(db_sales)


@router.delete("/{sale_id}", response_model=bool)
def delete_sale(
    sale_id: int,
    db: Database,
    sale_service: SaleService,
):
    """Delete sale by ID using dependency injection"""
    return sale_service.remove_sale(db, sale_id=sale_id)
