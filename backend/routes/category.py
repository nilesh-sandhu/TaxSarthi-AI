from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
    CategoryResponse,
)

from services.category import (
    create_category,
    get_categories,
    get_category,
    search_category,
    update_category,
    delete_category,
)

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)


# =====================================================
# Create Category
# =====================================================

@router.post(
    "/",
    response_model=CategoryResponse,
    status_code=201,
)
def add_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
):

    return create_category(
        category,
        db,
    )


# =====================================================
# Get All Categories
# =====================================================

@router.get(
    "/",
    response_model=list[CategoryResponse],
)
def all_categories(
    db: Session = Depends(get_db),
):

    return get_categories(db)


# =====================================================
# Search Categories
# =====================================================

@router.get(
    "/search/{keyword}",
    response_model=list[CategoryResponse],
)
def find_categories(
    keyword: str,
    db: Session = Depends(get_db),
):

    return search_category(
        keyword,
        db,
    )


# =====================================================
# Get Category By ID
# =====================================================

@router.get(
    "/{category_id}",
    response_model=CategoryResponse,
)
def single_category(
    category_id: int,
    db: Session = Depends(get_db),
):

    return get_category(
        category_id,
        db,
    )


# =====================================================
# Update Category
# =====================================================

@router.put(
    "/{category_id}",
    response_model=CategoryResponse,
)
def edit_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session = Depends(get_db),
):

    return update_category(
        category_id,
        category,
        db,
    )


# =====================================================
# Delete Category
# =====================================================

@router.delete(
    "/{category_id}",
)
def remove_category(
    category_id: int,
    db: Session = Depends(get_db),
):

    return delete_category(
        category_id,
        db,
    )