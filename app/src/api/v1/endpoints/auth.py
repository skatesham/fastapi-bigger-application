from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException
from jose import jwt

from app.src.api.deps import Database, UserService
from app.src.domain.user import schemas
from app.src.config import SECRET_KEY, ALGORITHM

router = APIRouter()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token with expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/login/", response_model=dict)
def login(
    user: schemas.UserCreate,
    db: Database,
    user_service: UserService,
):
    """User login endpoint"""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user and user.password == db_user.hashed_password:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"Authorization": "Bearer " + create_access_token(user.dict())}
