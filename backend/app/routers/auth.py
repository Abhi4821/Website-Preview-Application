from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    SignupRequest,
    TokenResponse,
    UserResponse,
)
from app.security import create_access_token, get_current_user
from app.services.auth_service import authenticate_user, create_user

router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def signup(
    payload: SignupRequest,
    db: Session = Depends(get_db),
):
    normalized_email = str(payload.email).strip().lower()

    existing = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    try:
        return create_user(
            db,
            payload.full_name,
            normalized_email,
            payload.password,
        )

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db),
):
    user = authenticate_user(
        db,
        str(payload.email),
        payload.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    return {
        "access_token": create_access_token(user.id),
        "token_type": "bearer",
        "user": user,
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def me(
    current_user: User = Depends(get_current_user),
):
    return current_user

# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.orm import Session

# from app.database import get_db
# from app.models.user import User
# from app.schemas.auth import LoginRequest, SignupRequest, TokenResponse, UserResponse
# from app.security import create_access_token, get_current_user
# from app.services.auth_service import authenticate_user, create_user

# router = APIRouter(prefix="/api/auth", tags=["Authentication"])


# @router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
# def signup(payload: SignupRequest, db: Session = Depends(get_db)):
#     existing = db.query(User).filter(User.email == payload.email.lower()).first()
#     if existing:
#         raise HTTPException(status_code=409, detail="An account with this email already exists.")
#     try:
#         return create_user(db, payload.full_name, payload.email, payload.password)
#     except IntegrityError:
#         db.rollback()
#         raise HTTPException(status_code=409, detail="An account with this email already exists.")


# @router.post("/login", response_model=TokenResponse)
# def login(payload: LoginRequest, db: Session = Depends(get_db)):
#     user = authenticate_user(db, payload.email, payload.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid email or password.")
#     return {
#         "access_token": create_access_token(user.id),
#         "token_type": "bearer",
#         "user": user,
#     }


# @router.get("/me", response_model=UserResponse)
# def me(current_user: User = Depends(get_current_user)):
#     return current_user
