from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class CarRepository(CRUDBase[models.Car, schemas.CarCreate, schemas.CarUpdate]):
    def __init__(self):
        super().__init__(models.Car)

    def get_by_brand(self, db: Session, *, brand: str) -> List[models.Car]:
        """Get cars by brand"""
        return db.query(self.model).filter(self.model.brand.ilike(f"%{brand}%")).all()

    def get_by_year(self, db: Session, *, year: int) -> List[models.Car]:
        """Get cars by year"""
        return db.query(self.model).filter(self.model.year == year).all()


# Create a singleton instance
car_repository = CarRepository()
