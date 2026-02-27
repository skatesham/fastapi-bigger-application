from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class UserRepository(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def __init__(self):
        super().__init__(models.User)

    def get_by_email(self, db: Session, *, email: str) -> Optional[models.User]:
        """Get user by email"""
        return db.query(self.model).filter(self.model.email == email).first()

    def get_active_users(self, db: Session) -> List[models.User]:
        """Get all active users"""
        return db.query(self.model).filter(self.model.is_active == True).all()

    def deactivate_user(self, db: Session, *, user_id: int) -> models.User:
        """Deactivate a user"""
        db_user = self.get_by_id(db, id=user_id)
        if db_user is None:
            raise ValueError(f"User with id {user_id} not found")
        
        db_user.is_active = False
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


class ItemRepository(CRUDBase[models.Item, schemas.ItemCreate, schemas.ItemUpdate]):
    def __init__(self):
        super().__init__(models.Item)

    def get_by_owner(self, db: Session, *, owner_id: int) -> List[models.Item]:
        """Get items by owner ID"""
        return db.query(self.model).filter(self.model.owner_id == owner_id).all()

    def search_by_title(self, db: Session, *, title: str) -> List[models.Item]:
        """Search items by title (partial match)"""
        return db.query(self.model).filter(
            self.model.title.ilike(f"%{title}%")
        ).all()


# Create singleton instances
user_repository = UserRepository()
item_repository = ItemRepository()
