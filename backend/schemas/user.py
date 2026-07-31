from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    mobile: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    mobile: str
    role: str

    class Config:
        from_attributes = True