from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.sale import service, schemas


router = APIRouter(
    prefix="/sales",
    tags=["sales"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Sale)
def create_sale(sale: schemas.SaleCreate, db: Session = Depends(get_db)):
    return service.create_sale(db=db, sale=sale)

@router.get("/{sale_id}", response_model=schemas.Sale)
def read_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return db_sale

@router.get("/", response_model=List[schemas.Sale])
def read_sales(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sales = service.get_sales(db, skip=skip, limit=limit)
    return sales

@router.delete("/{sale_id}", response_model=bool)
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    db_sale = service.get_sale(db, sale_id=sale_id)
    if db_sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return service.remove_sale(db, db_sale=db_sale)

