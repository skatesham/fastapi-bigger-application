from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class SellerRepository(CRUDBase[models.Seller, schemas.SellerCreate, schemas.SellerUpdate]):
    def __init__(self):
        super().__init__(models.Seller)

    def get_by_cpf(self, db: Session, *, cpf: str) -> Optional[models.Seller]:
        """Get seller by CPF"""
        return db.query(self.model).filter(self.model.cpf == cpf).first()

    def get_by_phone(self, db: Session, *, phone: str) -> Optional[models.Seller]:
        """Get seller by phone number"""
        return db.query(self.model).filter(self.model.phone == phone).first()

    def get_by_name(self, db: Session, *, name: str) -> List[models.Seller]:
        """Get sellers by name (partial match)"""
        return db.query(self.model).filter(
            self.model.name.ilike(f"%{name}%")
        ).all()


# Create a singleton instance
seller_repository = SellerRepository()
