from sqlalchemy.orm import Session

from . import exceptions, repository, schemas


class BuyerService:
    def __init__(self):
        self.buyer_repository = repository.buyer_repository

    def create_buyer(self, db: Session, buyer: schemas.BuyerCreate) -> schemas.Buyer:
        """Create a new buyer"""
        # Check if buyer with same phone already exists
        existing_buyer = self.buyer_repository.get_by_phone(db, phone=buyer.phone)
        if existing_buyer:
            raise exceptions.BuyerAlreadyExistsError("phone", buyer.phone)
        
        # Create buyer
        db_buyer = self.buyer_repository.create(db, obj_in=buyer)
        return schemas.Buyer.from_model(db_buyer)

    def get_buyer(self, db: Session, buyer_id: int) -> schemas.Buyer:
        """Get buyer by ID"""
        db_buyer = self.buyer_repository.get_by_id(db, id=buyer_id)
        if db_buyer is None:
            raise exceptions.BuyerNotFoundError(buyer_id)
        
        return schemas.Buyer.from_model(db_buyer)

    def get_buyers(self, db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Buyer]:
        """Get multiple buyers with pagination"""
        db_buyers = self.buyer_repository.get_multi(db, skip=skip, limit=limit)
        return schemas.Buyer.from_models(db_buyers)

    def update_buyer(self, db: Session, buyer_id: int, buyer_update: schemas.BuyerUpdate) -> schemas.Buyer:
        """Update buyer"""
        db_buyer = self.buyer_repository.get_by_id(db, id=buyer_id)
        if db_buyer is None:
            raise exceptions.BuyerNotFoundError(buyer_id)
        
        # Check if phone is being updated and already exists
        if buyer_update.phone and buyer_update.phone != db_buyer.phone:
            existing_buyer = self.buyer_repository.get_by_phone(db, phone=buyer_update.phone)
            if existing_buyer:
                raise exceptions.BuyerAlreadyExistsError("phone", buyer_update.phone)
        
        # Update buyer
        updated_buyer = self.buyer_repository.update(db, db_obj=db_buyer, obj_in=buyer_update)
        return schemas.Buyer.from_model(updated_buyer)

    def delete_buyer(self, db: Session, buyer_id: int) -> bool:
        """Delete buyer"""
        try:
            self.buyer_repository.delete(db, id=buyer_id)
            return True
        except ValueError:
            raise exceptions.BuyerNotFoundError(buyer_id)

    def search_buyers_by_name(self, db: Session, name: str) -> list[schemas.Buyer]:
        """Search buyers by name"""
        db_buyers = self.buyer_repository.get_by_name(db, name=name)
        return schemas.Buyer.from_models(db_buyers)


# Create singleton instance
buyer_service = BuyerService()
