import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


# ─── Base ────────────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)


# ─── Requests ────────────────────────────────────────────────────────────────

class UserRegister(UserBase):
    password: str = Field(min_length=8, max_length=64)

    @field_validator("password")
    @classmethod
    def password_strength(cls, value: str) -> str:
        if not any(c.isupper() for c in value):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in value):
            raise ValueError("Password must contain at least one digit")
        return value


class UserUpdate(BaseModel):
    first_name: str | None = Field(default=None, min_length=1, max_length=100)
    last_name: str | None = Field(default=None, min_length=1, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ─── Responses ───────────────────────────────────────────────────────────────

class UserResponse(UserBase):
    id: uuid.UUID
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class MessageResponse(BaseModel):
    message: str