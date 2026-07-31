from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from core.database import SessionLocal
from models.user import User
from schemas.user import UserCreate, UserResponse

router = APIRouter(tags=["Authentication"])


# Database Session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Register User
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):

    # Check email already exists
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        password=user.password,      # Hashing next step
        mobile=user.mobile
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user