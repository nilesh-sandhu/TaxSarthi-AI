from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.category import CategoryRepository
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


# =====================================================
# Create Category
# =====================================================

def create_category(
    category: CategoryCreate,
    db: Session,
):

    existing = CategoryRepository.get_by_name(
        db,
        category.name,
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Category already exists.",
        )

    return CategoryRepository.create(
        db,
        category,
    )


# =====================================================
# Get All Categories
# =====================================================

def get_categories(db: Session):

    return CategoryRepository.get_all(db)


# =====================================================
# Get Category By ID
# =====================================================

def get_category(
    category_id: int,
    db: Session,
):

    category = CategoryRepository.get_by_id(
        db,
        category_id,
    )

    if not category:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return category


# =====================================================
# Search Category
# =====================================================

def search_category(
    keyword: str,
    db: Session,
):

    categories = CategoryRepository.search(
        db,
        keyword,
    )

    if not categories:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No matching category found.",
        )

    return categories


# =====================================================
# Update Category
# =====================================================

def update_category(
    category_id: int,
    category: CategoryUpdate,
    db: Session,
):

    existing = CategoryRepository.get_by_id(
        db,
        category_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return CategoryRepository.update(
        db,
        existing,
        category,
    )


# =====================================================
# Delete Category
# =====================================================

def delete_category(
    category_id: int,
    db: Session,
):

    existing = CategoryRepository.get_by_id(
        db,
        category_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found.",
        )

    return CategoryRepository.delete(
        db,
        existing,
    )