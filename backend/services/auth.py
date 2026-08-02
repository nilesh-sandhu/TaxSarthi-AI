from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.user import User
from schemas.user import UserCreate
from core.security import hash_password, verify_password


def register_user(user: UserCreate, db: Session):

    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        mobile=user.mobile,
        hashed_password=hash_password(user.password),
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def login_user(email: str, password: str, db: Session):

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user is None:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user