from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import exceptions, repository, schemas


class SaleService:
    def __init__(self):
        self.sale_repository = repository.sale_repository

    def create_sale(self, db: Session, sale: schemas.SaleCreate) -> schemas.Sale:
        """Create a new sale"""
        # Validate that car exists
        from app.src.domain.car.repository import car_repository
        from app.src.domain.car.exceptions import CarNotFoundError
        car = car_repository.get_by_id(db, id=sale.car_id)
        if not car:
            raise CarNotFoundError(sale.car_id)
        
        # Validate that buyer exists
        from app.src.domain.buyer.repository import buyer_repository
        from app.src.domain.buyer.exceptions import BuyerNotFoundError
        buyer = buyer_repository.get_by_id(db, id=sale.buyer_id)
        if not buyer:
            raise BuyerNotFoundError(sale.buyer_id)
        
        # Validate that seller exists
        from app.src.domain.seller.repository import seller_repository
        from app.src.domain.seller.exceptions import SellerNotFoundError
        seller = seller_repository.get_by_id(db, id=sale.seller_id)
        if not seller:
            raise SellerNotFoundError(sale.seller_id)
        
        # Create sale using repository
        db_sale = self.sale_repository.create(db, obj_in=sale)
        return db_sale

    def get_sale(self, db: Session, sale_id: int) -> schemas.Sale:
        """Get sale by ID"""
        db_sale = self.sale_repository.get_by_id(db, id=sale_id)
        if db_sale is None:
            raise exceptions.SaleNotFoundError(sale_id)
        
        return db_sale

    def get_sales(self, db: Session) -> Page[schemas.Sale]:
        """Get all sales with pagination"""
        from .models import Sale
        return paginate(db, select(Sale).order_by(Sale.id))

    def update_sale(self, db: Session, sale_id: int, sale_update: schemas.SaleUpdate) -> schemas.Sale:
        """Update sale"""
        db_sale = self.sale_repository.get_by_id(db, id=sale_id)
        if db_sale is None:
            raise exceptions.SaleNotFoundError(sale_id)
        
        updated_sale = self.sale_repository.update(db, db_obj=db_sale, obj_in=sale_update)
        return updated_sale

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
        return db_sales

    def get_sales_by_buyer(self, db: Session, buyer_id: int) -> list[schemas.Sale]:
        """Get sales by buyer ID"""
        db_sales = self.sale_repository.get_by_buyer_id(db, buyer_id=buyer_id)
        return db_sales

    def get_sales_by_seller(self, db: Session, seller_id: int) -> list[schemas.Sale]:
        """Get sales by seller ID"""
        db_sales = self.sale_repository.get_by_seller_id(db, seller_id=seller_id)
        return db_sales


# Create singleton instance
sale_service = SaleService()
