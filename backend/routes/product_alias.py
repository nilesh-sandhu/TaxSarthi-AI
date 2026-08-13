from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.product_alias import (
    ProductAliasCreate,
    ProductAliasUpdate,
    ProductAliasResponse,
)

from services.product_alias import (
    create_alias,
    get_aliases,
    get_alias,
    search_alias,
    update_alias,
    delete_alias,
)

router = APIRouter(
    prefix="/product-alias",
    tags=["Product Alias"],
)


# =====================================================
# Create Alias
# =====================================================

@router.post(
    "/",
    response_model=ProductAliasResponse,
    status_code=201,
)
def add_alias(
    alias: ProductAliasCreate,
    db: Session = Depends(get_db),
):

    return create_alias(
        alias,
        db,
    )


# =====================================================
# Get All Aliases
# =====================================================

@router.get(
    "/",
    response_model=list[ProductAliasResponse],
)
def all_aliases(
    db: Session = Depends(get_db),
):

    return get_aliases(db)


# =====================================================
# Search Alias
# =====================================================

@router.get(
    "/search/{keyword}",
    response_model=list[ProductAliasResponse],
)
def find_alias(
    keyword: str,
    db: Session = Depends(get_db),
):

    return search_alias(
        keyword,
        db,
    )


# =====================================================
# Get Alias
# =====================================================

@router.get(
    "/{alias_id}",
    response_model=ProductAliasResponse,
)
def single_alias(
    alias_id: int,
    db: Session = Depends(get_db),
):

    return get_alias(
        alias_id,
        db,
    )


# =====================================================
# Update Alias
# =====================================================

@router.put(
    "/{alias_id}",
    response_model=ProductAliasResponse,
)
def edit_alias(
    alias_id: int,
    alias: ProductAliasUpdate,
    db: Session = Depends(get_db),
):

    return update_alias(
        alias_id,
        alias,
        db,
    )


# =====================================================
# Delete Alias
# =====================================================

@router.delete("/{alias_id}")
def remove_alias(
    alias_id: int,
    db: Session = Depends(get_db),
):

    return delete_alias(
        alias_id,
        db,
    )