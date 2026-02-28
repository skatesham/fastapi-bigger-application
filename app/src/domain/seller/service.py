from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import exceptions, repository, schemas


class SellerService:
    def __init__(self):
        self.seller_repository = repository.seller_repository

    def create_seller(self, db: Session, seller: schemas.SellerCreate) -> schemas.Seller:
        """Create a new seller"""
        # Check if seller with same CPF already exists
        existing_seller = self.seller_repository.get_by_cpf(db, cpf=seller.cpf)
        if existing_seller:
            raise exceptions.SellerAlreadyExistsError("cpf", seller.cpf)
        
        # Create seller
        db_seller = self.seller_repository.create(db, obj_in=seller)
        return db_seller

    def get_seller(self, db: Session, seller_id: int) -> schemas.Seller:
        """Get seller by ID"""
        db_seller = self.seller_repository.get_by_id(db, id=seller_id)
        if db_seller is None:
            raise exceptions.SellerNotFoundError(seller_id)
        
        return db_seller

    def get_sellers(self, db: Session) -> Page[schemas.Seller]:
        """Get all sellers with pagination"""
        from .models import Seller
        return paginate(db, select(Seller).order_by(Seller.id))

    def update_seller(self, db: Session, seller_id: int, seller_update: schemas.SellerUpdate) -> schemas.Seller:
        """Update seller"""
        db_seller = self.seller_repository.get_by_id(db, id=seller_id)
        if db_seller is None:
            raise exceptions.SellerNotFoundError(seller_id)
        
        # Check if CPF is being updated and already exists
        if seller_update.cpf and seller_update.cpf != db_seller.cpf:
            existing_seller = self.seller_repository.get_by_cpf(db, cpf=seller_update.cpf)
            if existing_seller:
                raise exceptions.SellerAlreadyExistsError("cpf", seller_update.cpf)
        
        # Update seller
        updated_seller = self.seller_repository.update(db, db_obj=db_seller, obj_in=seller_update)
        return schemas.Seller.from_model(updated_seller)

    def delete_seller(self, db: Session, seller_id: int) -> bool:
        """Delete seller"""
        try:
            self.seller_repository.delete(db, id=seller_id)
            return True
        except ValueError:
            raise exceptions.SellerNotFoundError(seller_id)

    def get_seller_by_cpf(self, db: Session, cpf: str) -> schemas.Seller:
        """Get seller by CPF"""
        db_seller = self.seller_repository.get_by_cpf(db, cpf=cpf)
        if db_seller is None:
            raise exceptions.SellerNotFoundError(0)  # CPF lookup, no ID
        
        return db_seller

    def search_sellers_by_name(self, db: Session, name: str) -> list[schemas.Seller]:
        """Search sellers by name"""
        db_sellers = self.seller_repository.get_by_name(db, name=name)
        return db_sellers


# Create singleton instance
seller_service = SellerService()
