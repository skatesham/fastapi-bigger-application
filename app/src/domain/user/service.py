from sqlalchemy.orm import Session

from . import exceptions, repository, schemas


class UserService:
    def __init__(self):
        self.user_repository = repository.user_repository
        self.item_repository = repository.item_repository

    def create_user(self, db: Session, user: schemas.UserCreate) -> schemas.User:
        """Create a new user"""
        # Check if user with same email already exists
        existing_user = self.user_repository.get_by_email(db, email=user.email)
        if existing_user:
            raise exceptions.UserAlreadyExistsError("email", user.email)
        
        # Create user (with fake hashing for now)
        fake_hashed_password = user.password + "notreallyhashed"
        user_data = user.model_dump()
        user_data["hashed_password"] = fake_hashed_password
        user_data.pop("password", None)  # Remove plain password
        
        db_user = self.user_repository.create(db, obj_in=schemas.UserCreate(**user_data))
        return schemas.User.model_validate(db_user)

    def get_user(self, db: Session, user_id: int) -> schemas.User:
        """Get user by ID"""
        db_user = self.user_repository.get_by_id(db, id=user_id)
        if db_user is None:
            raise exceptions.UserNotFoundError(user_id)
        
        return schemas.User.model_validate(db_user)

    def get_user_by_email(self, db: Session, email: str) -> schemas.User:
        """Get user by email"""
        db_user = self.user_repository.get_by_email(db, email=email)
        if db_user is None:
            raise exceptions.UserNotFoundError(0)  # Email lookup, no ID
        
        return schemas.User.model_validate(db_user)

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[schemas.User]:
        """Get multiple users with pagination"""
        db_users = self.user_repository.get_multi(db, skip=skip, limit=limit)
        return [schemas.User.model_validate(user) for user in db_users]

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
        updated_user = self.user_repository.update(db, db_obj=db_user, obj_in=schemas.UserUpdate(**update_data))
        return schemas.User.model_validate(updated_user)

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
        return schemas.User.model_validate(deactivated_user)

    def get_active_users(self, db: Session) -> list[schemas.User]:
        """Get all active users"""
        db_users = self.user_repository.get_active_users(db)
        return [schemas.User.model_validate(user) for user in db_users]

    # Item methods
    def create_user_item(self, db: Session, item: schemas.ItemCreate, user_id: int) -> schemas.Item:
        """Create item for user"""
        # Check if user exists and is active
        db_user = self.user_repository.get_by_id(db, id=user_id)
        if db_user is None:
            raise exceptions.UserNotFoundError(user_id)
        if not db_user.is_active:
            raise exceptions.InactiveUserError(user_id)
        
        # Create item
        item_data = item.model_dump()
        item_data["owner_id"] = user_id
        
        db_item = self.item_repository.create(db, obj_in=schemas.ItemCreate(**item_data))
        return schemas.Item.model_validate(db_item)

    def get_user_items(self, db: Session, user_id: int) -> list[schemas.Item]:
        """Get items by user ID"""
        db_items = self.item_repository.get_by_owner(db, owner_id=user_id)
        return [schemas.Item.model_validate(item) for item in db_items]

    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> list[schemas.Item]:
        """Get multiple items with pagination"""
        db_items = self.item_repository.get_multi(db, skip=skip, limit=limit)
        return [schemas.Item.model_validate(item) for item in db_items]


# Create singleton instances
user_service = UserService()
