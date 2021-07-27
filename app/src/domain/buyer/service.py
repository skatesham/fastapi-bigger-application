from sqlalchemy.orm import Session

from . import models, schemas

def create_buyer(db: Session, buyer: schemas.BuyerCreate):
    buyer_dict = buyer.dict()
    address_dict = buyer_dict["address"]
    db_buyer = models.Buyer(
        name=buyer_dict["name"],
        phone=buyer_dict["phone"],
        address_cep=address_dict["cep"],
        address_public_place=address_dict["public_place"],
        address_city=address_dict["city"],
        address_district=address_dict["district"],
        address_state=address_dict["state"],
    )
    
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

