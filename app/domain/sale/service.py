from sqlalchemy.orm import Session

from datetime import datetime

from . import models, schemas

def create_sale(db: Session, sale: schemas.SaleCreate):
    db_sale = models.Sale(**sale.dict(), created_at=str(datetime.now()))
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def get_sale(db: Session, sale_id: int):
    return db.query(models.Sale).filter(models.Sale.id == sale_id).first()

def get_sales(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Sale).offset(skip).limit(limit).all()

def remove_sale(db: Session, db_sale: models.Sale):
    db.delete(db_sale)
    db.commit()
    return True
