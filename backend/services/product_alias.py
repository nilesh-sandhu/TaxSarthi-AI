from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.product_alias import ProductAliasRepository
from schemas.product_alias import (
    ProductAliasCreate,
    ProductAliasUpdate,
)


# =====================================================
# Create Alias
# =====================================================

def create_alias(
    alias: ProductAliasCreate,
    db: Session,
):

    existing = ProductAliasRepository.get_by_alias(
        db,
        alias.alias,
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Alias already exists.",
        )

    return ProductAliasRepository.create(
        db,
        alias,
    )


# =====================================================
# Get All Aliases
# =====================================================

def get_aliases(
    db: Session,
):

    return ProductAliasRepository.get_all(db)


# =====================================================
# Get Alias By ID
# =====================================================

def get_alias(
    alias_id: int,
    db: Session,
):

    alias = ProductAliasRepository.get_by_id(
        db,
        alias_id,
    )

    if not alias:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alias not found.",
        )

    return alias


# =====================================================
# Search Alias
# =====================================================

def search_alias(
    keyword: str,
    db: Session,
):

    aliases = ProductAliasRepository.search(
        db,
        keyword,
    )

    if not aliases:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No aliases found.",
        )

    return aliases


# =====================================================
# Update Alias
# =====================================================

def update_alias(
    alias_id: int,
    alias: ProductAliasUpdate,
    db: Session,
):

    existing = ProductAliasRepository.get_by_id(
        db,
        alias_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alias not found.",
        )

    return ProductAliasRepository.update(
        db,
        existing,
        alias,
    )


# =====================================================
# Delete Alias
# =====================================================

def delete_alias(
    alias_id: int,
    db: Session,
):

    existing = ProductAliasRepository.get_by_id(
        db,
        alias_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alias not found.",
        )

    return ProductAliasRepository.delete(
        db,
        existing,
    )


# =====================================================
# Resolve Product (AI Search)
# =====================================================

def resolve_product(
    query: str,
    db: Session,
):

    alias = ProductAliasRepository.get_by_alias(
        db,
        query,
    )

    return alias