from typing import Optional, List

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class SaleRepository(CRUDBase[models.Sale, schemas.SaleCreate, schemas.SaleUpdate]):
    def __init__(self):
        super().__init__(models.Sale)

    def get_by_car_id(self, db: Session, *, car_id: int) -> List[models.Sale]:
        """Get sales by car ID"""
        return db.query(self.model).filter(self.model.car_id == car_id).all()

    def get_by_buyer_id(self, db: Session, *, buyer_id: int) -> List[models.Sale]:
        """Get sales by buyer ID"""
        return db.query(self.model).filter(self.model.buyer_id == buyer_id).all()

    def get_by_seller_id(self, db: Session, *, seller_id: int) -> List[models.Sale]:
        """Get sales by seller ID"""
        return db.query(self.model).filter(self.model.seller_id == seller_id).all()


# Create a singleton instance
sale_repository = SaleRepository()
