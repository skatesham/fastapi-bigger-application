from sqlalchemy.orm import Session

from . import models, schemas

def create_seller(db: Session, seller: schemas.SellerCreate):
    db_seller = models.Seller(**seller.dict())
    db.add(db_seller)
    db.commit()
    db.refresh(db_seller)
    return db_seller

def get_seller(db: Session, seller_id: int):
    return db.query(models.Seller).filter(models.Seller.id == seller_id).first()

def get_sellers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Seller).offset(skip).limit(limit).all()

def remove_seller(db: Session, db_seller: models.Seller):
    db.delete(db_seller)
    db.commit()
    return True

def get_by_cpf(db: Session, seller_cpf: str):
    return db.query(models.Seller).filter(models.Seller.cpf == seller_cpf).first()

