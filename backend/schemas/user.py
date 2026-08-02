from pydantic import BaseModel, EmailStr
from datetime import datetime


# -----------------------------
# User Registration
# -----------------------------
class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    mobile: str
    password: str


# -----------------------------
# User Login
# -----------------------------
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# -----------------------------
# User Response
# -----------------------------
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    mobile: str
    role: str
    created_at: datetime

    class Config:
        from_attributes = True