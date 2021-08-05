from typing import List

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.seller import service, schemas

from ...resources.strings import SELLER_DOES_NOT_EXIST_ERROR


router = APIRouter(
    prefix="/sellers",
    tags=["sellers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Seller, status_code=201)
def create_seller(seller: schemas.SellerCreate, db: Session = Depends(get_db)):
    return service.create_seller(db=db, seller=seller)

@router.get("/{seller_id}", response_model=schemas.Seller)
def read_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = service.get_seller(db, seller_id=seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail=SELLER_DOES_NOT_EXIST_ERROR)
    return db_seller

@router.get("/cpf/{seller_cpf}", response_model=schemas.Seller)
def read_seller_by_cpf(seller_cpf: str, db: Session = Depends(get_db)):
    db_seller = service.get_by_cpf(db, seller_cpf=seller_cpf)
    if db_seller is None:
        raise HTTPException(status_code=404, detail=SELLER_DOES_NOT_EXIST_ERROR)
    return db_seller

@router.get("/", response_model=List[schemas.Seller])
def read_sellers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sellers = service.get_sellers(db, skip=skip, limit=limit)
    return sellers

@router.delete("/{seller_id}", response_model=bool)
def delete_seller(seller_id: int, db: Session = Depends(get_db)):
    db_seller = service.get_seller(db, seller_id=seller_id)
    if db_seller is None:
        raise HTTPException(status_code=404, detail=SELLER_DOES_NOT_EXIST_ERROR)
    return service.remove_seller(db, db_seller=db_seller)
