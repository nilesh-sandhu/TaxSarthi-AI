from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.product_master import (
    ProductMasterCreate,
    ProductMasterUpdate,
    ProductMasterResponse,
)

from services.product_master import (
    create_product,
    get_products,
    get_product,
    search_product,
    update_product,
    delete_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Product Master"],
)


# =====================================================
# Create Product
# =====================================================

@router.post(
    "/",
    response_model=ProductMasterResponse,
    status_code=201,
)
def add_product(
    product: ProductMasterCreate,
    db: Session = Depends(get_db),
):

    return create_product(
        product,
        db,
    )


# =====================================================
# Get All Products
# =====================================================

@router.get(
    "/",
    response_model=list[ProductMasterResponse],
)
def all_products(
    db: Session = Depends(get_db),
):

    return get_products(db)


# =====================================================
# Search Product
# =====================================================

@router.get(
    "/search/{keyword}",
    response_model=list[ProductMasterResponse],
)
def find_product(
    keyword: str,
    db: Session = Depends(get_db),
):

    return search_product(
        keyword,
        db,
    )


# =====================================================
# Get Product By ID
# =====================================================

@router.get(
    "/{product_id}",
    response_model=ProductMasterResponse,
)
def single_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    return get_product(
        product_id,
        db,
    )


# =====================================================
# Update Product
# =====================================================

@router.put(
    "/{product_id}",
    response_model=ProductMasterResponse,
)
def edit_product(
    product_id: int,
    product: ProductMasterUpdate,
    db: Session = Depends(get_db),
):

    return update_product(
        product_id,
        product,
        db,
    )


# =====================================================
# Delete Product
# =====================================================

@router.delete(
    "/{product_id}",
)
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
):

    return delete_product(
        product_id,
        db,
    )