from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from services.search import universal_search

router = APIRouter(
    prefix="/search",
    tags=["Universal Search"],
)


# ---------------------------------
# Universal Search
# ---------------------------------
@router.get("/")
def search(
    q: str,
    db: Session = Depends(get_db),
):

    return universal_search(q, db)