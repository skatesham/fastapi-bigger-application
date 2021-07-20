from sqlalchemy.orm import Session

from . import models, schemas

def create_buyer(db: Session, buyer: schemas.BuyerCreate):
    db_buyer = models.Buyer(**buyer.dict())
    db.add(db_buyer)
    db.commit()
    db.refresh(db_buyer)
    return db_buyer

def get_buyer(db: Session, buyer_id: int):
    return db.query(models.Buyer).filter(models.Buyer.id == buyer_id).first()

def get_buyers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Buyer).offset(skip).limit(limit).all()

def remove_buyer(db: Session, db_buyer: models.Buyer):
    db.delete(db_buyer)
    db.commit()
    return True

