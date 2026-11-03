from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.saved_url import SavedURL
from app.models.user import User
from app.schemas.saved_url import PreviewRequest, SavedURLResponse
from app.security import get_current_user
from app.services.preview_service import fetch_preview

router = APIRouter(prefix="/api/urls", tags=["Saved URLs"])


@router.post("/preview", response_model=SavedURLResponse, status_code=status.HTTP_201_CREATED)
def create_preview(
    payload: PreviewRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    try:
        metadata = fetch_preview(str(payload.url))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=502, detail="Could not fetch this website. It may block automated requests.")

    saved = SavedURL(user_id=current_user.id, **metadata)
    db.add(saved)
    db.commit()
    db.refresh(saved)
    return saved


@router.get("", response_model=list[SavedURLResponse])
def list_urls(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(SavedURL)
        .filter(SavedURL.user_id == current_user.id)
        .order_by(SavedURL.created_at.desc())
        .all()
    )


@router.get("/{url_id}", response_model=SavedURLResponse)
def get_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    saved = db.query(SavedURL).filter(
        SavedURL.id == url_id, SavedURL.user_id == current_user.id
    ).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved URL not found.")
    return saved


@router.delete("/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(
    url_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    saved = db.query(SavedURL).filter(
        SavedURL.id == url_id, SavedURL.user_id == current_user.id
    ).first()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved URL not found.")
    db.delete(saved)
    db.commit()
    return None
