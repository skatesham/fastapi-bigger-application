from typing import List, Optional

from sqlalchemy.orm import Session

from app.src.core.repository import CRUDBase
from . import models, schemas


class UserRepository(CRUDBase[models.User, dict, schemas.UserUpdate]):
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


# Create singleton instance
user_repository = UserRepository()
