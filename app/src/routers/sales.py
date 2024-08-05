from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .converter import sale_converter
from ..dependencies import get_db
from ..domain.buyer import service as buyer_service
from ..domain.car import repository as car_repository
from ..domain.sale import service, schemas
from ..domain.seller import service as seller_service
from ..domain.stock import service as stock_service
from ...resources.strings import BUYER_DOES_NOT_EXIST_ERROR
from ...resources.strings import CAR_DOES_NOT_EXIST_ERROR
from ...resources.strings import SALES_DOES_NOT_EXIST_ERROR
from ...resources.strings import SELLER_DOES_NOT_EXIST_ERROR
from ...resources.strings import STOCK_DOES_NOT_EXIST_ERROR

router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=schemas.Sale, status_code=201)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
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
    db_sale = service.create_sale(db=db, sale=sale)
    return sale_converter.convert(db_sale)


@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)
    return sale_converter.convert(db_sale)


@router.get("/", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = service.get_sales(db, skip=skip, limit=limit)
    return sale_converter.convert_many(sales)


@router.delete("/{sale_id}", response_model=bool)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail=SALES_DOES_NOT_EXIST_ERROR)
    return service.remove_sale(db, db_sale=db_sale)
