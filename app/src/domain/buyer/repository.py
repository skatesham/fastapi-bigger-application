from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class BuyerRepository(CRUDBase[models.Buyer, schemas.BuyerCreate, schemas.BuyerUpdate]):
    def __init__(self):
        super().__init__(models.Buyer)

    def create(self, db: Session, *, obj_in: schemas.BuyerCreate) -> models.Buyer:
        """Create buyer with address flattening"""
        obj_data = obj_in.model_dump()
        address_data = obj_data.pop("address", {})
        
        # Flatten address into buyer fields
        buyer_data = {
            **obj_data,
            "address_cep": address_data.get("cep"),
            "address_public_place": address_data.get("public_place"),
            "address_city": address_data.get("city"),
            "address_district": address_data.get("district"),
            "address_state": address_data.get("state"),
        }
        
        db_obj = self.model(**buyer_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[models.Buyer]:
        """Get buyer by phone number"""
        return db.query(self.model).filter(self.model.phone == phone).first()

    def get_by_name(self, db: Session, *, name: str) -> List[models.Buyer]:
        """Get buyers by name (partial match)"""
        return db.query(self.model).filter(
            self.model.name.ilike(f"%{name}%")
        ).all()


# Create a singleton instance
buyer_repository = BuyerRepository()
