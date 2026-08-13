from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.jwt import create_access_token
from core.config import settings
from schemas.user import UserCreate, UserLogin, UserResponse
from schemas.token import Token
from services.auth import register_user, login_user, google_login
from dependencies.auth import get_current_user
from models.user import User

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    return register_user(user, db)


@router.post(
    "/login",
    response_model=Token,
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db),
):
    authenticated_user = login_user(
        user.email,
        user.password,
        db,
    )

    if authenticated_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    return Token(
        access_token=create_access_token(
            data={"sub": authenticated_user.email}
        ),
        token_type="bearer",
    )


@router.post(
    "/google",
    response_model=Token,
)
def google_sign_in(
    payload: dict,
    db: Session = Depends(get_db),
):
    credential = payload.get("credential")

    if not credential:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Google credential is required.",
        )

    client_id = getattr(
        settings,
        "GOOGLE_CLIENT_ID",
        None,
    )

    if not client_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Google Sign-In is not configured on the server.",
        )

    user = google_login(
        credential,
        db,
        client_id,
    )

    return Token(
        access_token=create_access_token(
            data={"sub": user.email}
        ),
        token_type="bearer",
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user
