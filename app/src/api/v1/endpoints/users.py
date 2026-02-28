from typing import List
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate

from fastapi import APIRouter, HTTPException

from app.src.api.deps import Database, UserService
from app.src.domain.user import exceptions, schemas
from app.resources.strings import USER_ALREADY_EXISTS_ERROR, USER_DOES_NOT_EXIST_ERROR, INVALID_USER_ERROR

router = APIRouter()


@router.post("/", response_model=schemas.User, status_code=201)
def create_user(
    user: schemas.UserCreate,
    db: Database,
    user_service: UserService,
):
    """Create new user using dependency injection"""
    try:
        return(user_service).create_user(db=db, user=user)
    except exceptions.UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=USER_ALREADY_EXISTS_ERROR)
    except exceptions.InvalidUserError as e:
        raise HTTPException(status_code=400, detail=INVALID_USER_ERROR)


@router.get("/{user_id}", response_model=schemas.User)
def read_user(
    user_id: int,
    db: Database,
    user_service: UserService,
):
    """Get user by ID using dependency injection"""
    try:
        return(user_service).get_user(db, user_id=user_id)
    except exceptions.UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=USER_DOES_NOT_EXIST_ERROR)


@router.get("/", response_model=Page[schemas.User])
def read_users(
    db: Database,
    user_service: UserService,
):
    """Get all users with automatic pagination"""
    return user_service.get_users(db)
