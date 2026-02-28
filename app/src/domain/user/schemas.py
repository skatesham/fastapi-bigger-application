from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")
    is_active: Optional[bool] = True


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, description="Password must be at least 8 characters long")
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
