from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from . import exceptions, repository, schemas


class UserService:
    def __init__(self):
        self.user_repository = repository.user_repository

    def create_user(self, db: Session, user: schemas.UserCreate) -> schemas.User:
        """Create a new user"""
        # Check if user with same email already exists
        existing_user = self.user_repository.get_by_email(db, email=user.email)
        if existing_user:
            raise exceptions.UserAlreadyExistsError("email", user.email)
        
        # Create user (with fake hashing for now)
        fake_hashed_password = user.password + "notreallyhashed"
        
        # Create user directly with model data
        from .models import User
        db_user = User(
            email=user.email,
            hashed_password=fake_hashed_password,
            is_active=user.is_active if user.is_active is not None else True
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def get_user(self, db: Session, user_id: int) -> schemas.User:
        """Get user by ID"""
        db_user = self.user_repository.get_by_id(db, id=user_id)
        if db_user is None:
            raise exceptions.UserNotFoundError(user_id)
        
        return db_user

    def get_user_by_email(self, db: Session, email: str) -> schemas.User:
        """Get user by email"""
        db_user = self.user_repository.get_by_email(db, email=email)
        if db_user is None:
            raise exceptions.UserNotFoundError(0)  # Email lookup, no ID
        
        return db_user

    def get_users(self, db: Session) -> Page[schemas.User]:
        """Get all users with pagination"""
        from .models import User
        return paginate(db, select(User).order_by(User.id))

    def update_user(self, db: Session, user_id: int, user_update: schemas.UserUpdate) -> schemas.User:
        """Update user"""
        db_user = self.user_repository.get_by_id(db, id=user_id)
        if db_user is None:
            raise exceptions.UserNotFoundError(user_id)
        
        # Check if email is being updated and already exists
        if user_update.email and user_update.email != db_user.email:
            existing_user = self.user_repository.get_by_email(db, email=user_update.email)
            if existing_user:
                raise exceptions.UserAlreadyExistsError("email", user_update.email)
        
        # Handle password update
        update_data = user_update.model_dump(exclude_unset=True)
        if "password" in update_data:
            update_data["hashed_password"] = update_data.pop("password") + "notreallyhashed"
        
        # Update user
        updated_user = self.user_repository.update(db, db_obj=db_user, obj_in=update_data)
        return updated_user

    def delete_user(self, db: Session, user_id: int) -> bool:
        """Delete user"""
        try:
            self.user_repository.delete(db, id=user_id)
            return True
        except ValueError:
            raise exceptions.UserNotFoundError(user_id)

    def deactivate_user(self, db: Session, user_id: int) -> schemas.User:
        """Deactivate a user"""
        db_user = self.user_repository.get_by_id(db, id=user_id)
        if db_user is None:
            raise exceptions.UserNotFoundError(user_id)
        
        deactivated_user = self.user_repository.deactivate_user(db, user_id=user_id)
        return deactivated_user

    def get_active_users(self, db: Session) -> list[schemas.User]:
        """Get all active users"""
        db_users = self.user_repository.get_active_users(db)
        return db_users


# Create singleton instances
user_service = UserService()
