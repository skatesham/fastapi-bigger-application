from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException

from ...deps import Database, UserService
from ....domain.user import schemas
from ....core.security import create_access_token, SECRET_KEY, ALGORITHM
from app.resources.strings import EMAIL_ALREADY_REGISTERED_ERROR

router = APIRouter()


@router.post("/login/", response_model=dict)
def login(
    user: schemas.UserCreate,
    db: Database,
    user_service: UserService,
):
    """User login endpoint"""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user and user.password == db_user.hashed_password:
        raise HTTPException(status_code=400, detail=EMAIL_ALREADY_REGISTERED_ERROR)
    return {"Authorization": "Bearer " + create_access_token(user.dict())}
