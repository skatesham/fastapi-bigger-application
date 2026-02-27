from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class StockRepository(CRUDBase[models.Stock, schemas.StockCreate, schemas.StockUpdate]):
    def __init__(self):
        super().__init__(models.Stock)

    def get_by_car_id(self, db: Session, *, car_id: int) -> Optional[models.Stock]:
        """Get stock by car ID"""
        return db.query(self.model).filter(self.model.car_id == car_id).first()

    def get_low_stock(self, db: Session, *, threshold: int = 5) -> List[models.Stock]:
        """Get stocks with quantity below threshold"""
        return db.query(self.model).filter(
            self.model.quantity <= threshold
        ).all()

    def get_available_stock(self, db: Session) -> List[models.Stock]:
        """Get all stocks with quantity > 0"""
        return db.query(self.model).filter(
            self.model.quantity > 0
        ).all()

    def update_quantity(self, db: Session, *, stock_id: int, new_quantity: int) -> models.Stock:
        """Update stock quantity directly"""
        db_stock = self.get_by_id(db, id=stock_id)
        if db_stock is None:
            raise ValueError(f"Stock with id {stock_id} not found")
        
        db_stock.quantity = new_quantity
        db.add(db_stock)
        db.commit()
        db.refresh(db_stock)
        return db_stock


# Create a singleton instance
stock_repository = StockRepository()
