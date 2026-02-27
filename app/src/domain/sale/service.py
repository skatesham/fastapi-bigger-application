from sqlalchemy.orm import Session

from . import exceptions, repository, schemas


class SaleService:
    def __init__(self):
        self.sale_repository = repository.sale_repository

    def create_sale(self, db: Session, sale: schemas.SaleCreate) -> schemas.Sale:
        """Create a new sale"""
        # Create sale using repository
        db_sale = self.sale_repository.create(db, obj_in=sale)
        return schemas.Sale.from_model(db_sale)

    def get_sale(self, db: Session, sale_id: int) -> schemas.Sale:
        """Get sale by ID"""
        db_sale = self.sale_repository.get_by_id(db, id=sale_id)
        if db_sale is None:
            raise exceptions.SaleNotFoundError(sale_id)
        
        return schemas.Sale.from_model(db_sale)

    def get_sales(self, db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Sale]:
        """Get multiple sales with pagination"""
        db_sales = self.sale_repository.get_multi(db, skip=skip, limit=limit)
        return schemas.Sale.from_models(db_sales)

    def update_sale(self, db: Session, sale_id: int, sale_update: schemas.SaleUpdate) -> schemas.Sale:
        """Update sale"""
        db_sale = self.sale_repository.get_by_id(db, id=sale_id)
        if db_sale is None:
            raise exceptions.SaleNotFoundError(sale_id)
        
        updated_sale = self.sale_repository.update(db, db_obj=db_sale, obj_in=sale_update)
        return schemas.Sale.from_model(updated_sale)

    def delete_sale(self, db: Session, sale_id: int) -> bool:
        """Delete sale"""
        try:
            self.sale_repository.delete(db, id=sale_id)
            return True
        except ValueError:
            raise exceptions.SaleNotFoundError(sale_id)

    def get_sales_by_car(self, db: Session, car_id: int) -> list[schemas.Sale]:
        """Get sales by car ID"""
        db_sales = self.sale_repository.get_by_car_id(db, car_id=car_id)
        return schemas.Sale.from_models(db_sales)

    def get_sales_by_buyer(self, db: Session, buyer_id: int) -> list[schemas.Sale]:
        """Get sales by buyer ID"""
        db_sales = self.sale_repository.get_by_buyer_id(db, buyer_id=buyer_id)
        return schemas.Sale.from_models(db_sales)

    def get_sales_by_seller(self, db: Session, seller_id: int) -> list[schemas.Sale]:
        """Get sales by seller ID"""
        db_sales = self.sale_repository.get_by_seller_id(db, seller_id=seller_id)
        return schemas.Sale.from_models(db_sales)


# Create singleton instance
sale_service = SaleService()
