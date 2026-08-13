from pydantic import BaseModel, EmailStr
from datetime import datetime


# ============================
# Register
# ============================

class UserCreate(BaseModel):

    full_name: str

    email: EmailStr

    mobile: str

    password: str


# ============================
# Login
# ============================

class UserLogin(BaseModel):

    email: EmailStr

    password: str


# ============================
# Response
# ============================

class UserResponse(BaseModel):

    id: int

    full_name: str

    email: str

    mobile: str

    role: str

    created_at: datetime

    class Config:
        from_attributes = True