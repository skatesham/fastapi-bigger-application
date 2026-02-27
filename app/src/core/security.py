"""
Security module for FastAPI application
JWT token handling and authentication utilities
"""

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Header, HTTPException
from jose import jwt

from .config import SECRET_KEY, ALGORITHM


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    """Decode JWT token and return payload"""
    stripped_token = token.replace("Bearer ", "")
    return jwt.decode(stripped_token, SECRET_KEY, algorithms=[ALGORITHM])


async def get_token_header(x_token: str = Header(...)) -> dict:
    """Example header validation dependency"""
    payload = decode_token(x_token)
    username: str = payload.get("email")
    if username is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return payload


async def get_query_token(token: str) -> str:
    """Example query token validation"""
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    return token


# Type aliases for dependency injection
TokenHeader = Optional[dict]
QueryToken = Optional[str]
