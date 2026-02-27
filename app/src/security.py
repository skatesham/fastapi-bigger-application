"""
Security and Authentication Dependencies
JWT token handling and validation
"""

from datetime import datetime, timedelta
from typing import Annotated, Optional

from fastapi import Depends, Header, HTTPException
from jose import jwt

# Security Configuration
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"


def decode(token: str) -> dict:
    """Decode JWT token"""
    stripped_token = token.replace("Bearer ", "")
    return jwt.decode(stripped_token, SECRET_KEY, algorithms=[ALGORITHM])


def encode() -> str:
    """Encode JWT token"""
    return jwt.encode({"some": "payload"}, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create access token with expiration"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Token Dependencies
async def get_token_header(x_token: str = Header(...)) -> dict:
    """Example header validation dependency"""
    payload = decode(x_token)
    username: str = payload.get("email")
    if username is None:
        raise HTTPException(status_code=403, detail="Unauthorized")
    return payload


async def get_query_token(token: str) -> str:
    """Example query token validation"""
    if token != "jessica":
        raise HTTPException(status_code=400, detail="No Jessica token provided")
    return token


# Annotated Dependencies for clean injection
TokenHeader = Annotated[dict, Depends(get_token_header)]
QueryToken = Annotated[str, Depends(get_query_token)]
