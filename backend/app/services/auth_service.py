from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.security import hash_password, verify_password


def create_user(
    db: Session,
    full_name: str,
    email: str,
    password: str,
) -> User:
    user = User(
        full_name=full_name.strip(),
        email=email.strip().lower(),
        hashed_password=hash_password(password),
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    except IntegrityError:
        db.rollback()
        raise

    except Exception:
        db.rollback()
        raise


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> User | None:
    normalized_email = email.strip().lower()

    user = (
        db.query(User)
        .filter(User.email == normalized_email)
        .first()
    )

    if user is None or not user.is_active:
        return None

    if not verify_password(password, user.hashed_password):
        return None

    return user


# from sqlalchemy.orm import Session

# from app.models.user import User
# from app.security import hash_password, verify_password


# def create_user(db: Session, full_name: str, email: str, password: str) -> User:
#     user = User(
#         full_name=full_name.strip(),
#         email=email.lower().strip(),
#         hashed_password=hash_password(password),
#     )
#     db.add(user)
#     db.commit()
#     db.refresh(user)
#     return user


# def authenticate_user(db: Session, email: str, password: str) -> User | None:
#     user = db.query(User).filter(User.email == email.lower().strip()).first()
#     if user is None or not user.is_active:
#         return None
#     if not verify_password(password, user.hashed_password):
#         return None
#     return user
