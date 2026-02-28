from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException, Query
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from app.src.api.deps import Database, SaleService, StockService
from app.src.domain.sale import exceptions as sale_exceptions
from app.src.domain.car import exceptions as car_exceptions
from app.src.domain.buyer import exceptions as buyer_exceptions
from app.src.domain.seller import exceptions as seller_exceptions
from app.src.domain.stock import exceptions as stock_exceptions
from app.src.domain.sale import schemas
from app.resources.strings import SALES_ALREADY_EXISTS_ERROR, SALES_DOES_NOT_EXIST_ERROR, INVALID_SALE_ERROR

router = APIRouter()


@router.post("/", response_model=schemas.Sale, status_code=201)
def create_sale(
    sale: schemas.SaleCreate,
    db: Database,
    sale_service: SaleService,
    stock_service: StockService,
):
    """Create new sale using dependency injection"""
    try:
        # Reduce stock quantity
        stock_service.buy_car_from_stock(db, car_id=sale.car_id, quantity=1)
        db_sale = sale_service.create_sale(db=db, sale=sale)
        return db_sale
    except car_exceptions.CarNotFoundError as e:
        raise HTTPException(status_code=404, detail="car does not exist")
    except buyer_exceptions.BuyerNotFoundError as e:
        raise HTTPException(status_code=404, detail="buyer does not exist")
    except seller_exceptions.SellerNotFoundError as e:
        raise HTTPException(status_code=404, detail="seller does not exist")
    except stock_exceptions.StockNotFoundError as e:
        raise HTTPException(status_code=404, detail="stock does not exist")
    except stock_exceptions.InsufficientStockError as e:
        raise HTTPException(status_code=422, detail="out of stock")
    except sale_exceptions.SaleNotFoundError as e:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)
    except sale_exceptions.InvalidSaleError as e:
        raise HTTPException(status_code=400, detail=INVALID_SALE_ERROR)


@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(
    sale_id: int,
    db: Database,
    sale_service: SaleService,
):
    """Get sale by ID using dependency injection"""
    try:
        db_sale = sale_service.get_sale(db, sale_id=sale_id)
        return db_sale
    except sale_exceptions.SaleNotFoundError as e:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=Page[schemas.Sale])
def read_sales(
    db: Database,
    sale_service: SaleService,
):
    """Get all sales with automatic pagination"""
    return sale_service.get_sales(db)


@router.delete("/{sale_id}", response_model=bool)
def delete_sale(
    sale_id: int,
    db: Database,
    sale_service: SaleService,
):
    """Delete sale by ID using dependency injection"""
    try:
        return sale_service.delete_sale(db, sale_id=sale_id)
    except sale_exceptions.SaleNotFoundError as e:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)


@router.get("/search/by-car/", response_model=List[schemas.Sale])
def search_sales_by_car(
    db: Database,
    sale_service: SaleService,
    car_id: int = Query(..., description="Search sales by car ID"),
):
    """Get sales by car ID"""
    return sale_service.get_sales_by_car(db, car_id=car_id)


@router.get("/search/by-buyer/", response_model=List[schemas.Sale])
def search_sales_by_buyer(
    db: Database,
    sale_service: SaleService,
    buyer_id: int = Query(..., description="Search sales by buyer ID"),
):
    """Get sales by buyer ID"""
    return sale_service.get_sales_by_buyer(db, buyer_id=buyer_id)


@router.get("/search/by-seller/", response_model=List[schemas.Sale])
def search_sales_by_seller(
    db: Database,
    sale_service: SaleService,
    seller_id: int = Query(..., description="Search sales by seller ID"),
):
    """Get sales by seller ID"""
    return sale_service.get_sales_by_seller(db, seller_id=seller_id)
