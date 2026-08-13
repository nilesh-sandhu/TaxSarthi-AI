from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from core.security import hash_password, verify_password
from models.user import User
from schemas.user import UserCreate


def register_user(user: UserCreate, db: Session):
    existing_user = db.query(User).filter(
        (User.email == user.email) |
        (User.mobile == user.mobile)
    ).first()

    if existing_user:
        if existing_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered.",
        )

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        mobile=user.mobile,
        hashed_password=hash_password(user.password),
        role="user",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(email: str, password: str, db: Session):
    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password
    ):
        return None

    return user


def google_login(
    credential: str,
    db: Session,
    google_client_id: str,
):
    try:
        info = id_token.verify_oauth2_token(
            credential,
            google_requests.Request(),
            google_client_id,
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Google sign-in credential.",
        )

    email = info.get("email")
    name = info.get("name") or "Google User"
    google_sub = info.get("sub")

    if not email or not google_sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google account information is incomplete.",
        )

    if info.get("email_verified") is not True:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Google email is not verified.",
        )

    user = db.query(User).filter(
        User.email == email
    ).first()

    if user:
        return user

    # Current User model requires mobile/password.
    # These internal values are only for the Google-created account.
    new_user = User(
        full_name=name[:100],
        email=email,
        mobile=f"google:{google_sub}"[:20],
        hashed_password=hash_password(
            f"google-{google_sub}"
        ),
        role="user",
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
