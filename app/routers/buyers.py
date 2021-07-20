from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..dependencies import get_db

from ..domain.buyer import service, schemas


router = APIRouter(
    prefix="/buyers",
    tags=["buyers"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.Buyer)
def create_buyer(buyer: schemas.BuyerCreate, db: Session = Depends(get_db)):
    return service.create_buyer(db=db, buyer=buyer)

@router.get("/{buyer_id}", response_model=schemas.Buyer)
def read_buyer(buyer_id: int, db: Session = Depends(get_db)):
    db_buyer = service.get_buyer(db, buyer_id=buyer_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer Model not found")
    return db_buyer

@router.get("/", response_model=List[schemas.Buyer])
def read_buyers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buyers = service.get_buyers(db, skip=skip, limit=limit)
    return buyers

@router.delete("/{buyer_id}", response_model=bool)
def delete_buyer(buyer_id: int, db: Session = Depends(get_db)):
    db_buyer = service.get_buyer(db, buyer_id=buyer_id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return service.remove_buyer(db, db_buyer=db_buyer)
