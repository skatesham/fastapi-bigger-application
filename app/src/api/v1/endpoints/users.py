from typing import List

from fastapi import APIRouter

from ...deps import Database, UserService
from ....domain.user import schemas

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Database,
    user_service: UserService,
):
    """Create new user using dependency injection"""
    return user_service.create_user(db=db, user=user)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Database,
    user_service: UserService,
):
    """Get user by ID using dependency injection"""
    return user_service.get_user(db, user_id=user_id)


@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Database,
    user_service: UserService,
    skip: int = 0,
    limit: int = 100,
):
    """Get all users with pagination using dependency injection"""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users
