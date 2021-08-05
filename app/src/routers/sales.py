from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.sale import service, schemas, models

from ..domain.car import service as car_service

from ..domain.buyer import service as buyer_service

from ..domain.seller import service as seller_service

from ..domain.stock import service as stock_service

from .converter import sale_converter


router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Sale, status_code=201)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    if car_service.get_car(db, car_id=sale.car_id) is None:
        raise HTTPException(status_code=404, detail="car does not found")
    if buyer_service.get_buyer(db, buyer_id=sale.buyer_id) is None:
        raise HTTPException(status_code=404, detail="buyer not found")
    if seller_service.get_seller(db, seller_id=sale.seller_id) is None:
        raise HTTPException(status_code=404, detail="seller not found")
    if stock_service.get_stock_by_car(db, car_id=sale.car_id) is None:
        raise HTTPException(status_code=404, detail="stock not found")
    
    stock_service.buy_car_from_stock(db, car_id=sale.car_id, quantity=1)
    db_sale = service.create_sale(db=db, sale=sale)
    return sale_converter.convert(db_sale)

@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="sale not found")
    return sale_converter.convert(db_sale)

@router.get("/", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = service.get_sales(db, skip=skip, limit=limit)
    return sale_converter.convert_many(sales)

@router.delete("/{sale_id}", response_model=bool)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="sale not found")
    return service.remove_sale(db, db_sale=db_sale)

