from datetime import timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from ...deps import Database, UserService
from ....domain.user import schemas
from ....core.security import (
    create_access_token, 
    verify_password, 
    get_password_hash,
    get_current_user
)
from ....core.config import settings
from app.resources.strings import EMAIL_ALREADY_REGISTERED_ERROR

router = APIRouter()


@router.post("/login/", response_model=dict)
async def login(
    db: Database,
    user_service: UserService,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """User login endpoint"""
    # Authenticate user
    user = user_service.get_user_by_email(db, email=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/register/", response_model=dict)
async def register(
    db: Database,
    user_service: UserService,
    user: schemas.UserCreate,
):
    """User registration endpoint"""
    # Check if user already exists
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=EMAIL_ALREADY_REGISTERED_ERROR
        )
    
    # Hash password and create user
    user.hashed_password = get_password_hash(user.hashed_password)
    db_user = user_service.create_user(db=db, user=user)
    
    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.get("/me/", response_model=dict)
async def read_users_me(current_user: dict = Depends(get_current_user)):
    """Get current user info"""
    return current_user
