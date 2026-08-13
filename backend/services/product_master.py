from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.product_master import ProductMasterRepository
from schemas.product_master import (
    ProductMasterCreate,
    ProductMasterUpdate,
)


# =====================================================
# Create Product
# =====================================================

def create_product(
    product: ProductMasterCreate,
    db: Session,
):

    existing = ProductMasterRepository.get_by_name(
        db,
        product.product_name,
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product already exists.",
        )

    return ProductMasterRepository.create(
        db,
        product,
    )


# =====================================================
# Get All Products
# =====================================================

def get_products(db: Session):

    return ProductMasterRepository.get_all(db)


# =====================================================
# Get Product
# =====================================================

def get_product(
    product_id: int,
    db: Session,
):

    product = ProductMasterRepository.get_by_id(
        db,
        product_id,
    )

    if not product:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return product


# =====================================================
# Search Product
# =====================================================

def search_product(
    keyword: str,
    db: Session,
):

    return ProductMasterRepository.search(
        db,
        keyword,
    )


# =====================================================
# Update Product
# =====================================================

def update_product(
    product_id: int,
    product: ProductMasterUpdate,
    db: Session,
):

    existing = ProductMasterRepository.get_by_id(
        db,
        product_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return ProductMasterRepository.update(
        db,
        existing,
        product,
    )


# =====================================================
# Delete Product
# =====================================================

def delete_product(
    product_id: int,
    db: Session,
):

    existing = ProductMasterRepository.get_by_id(
        db,
        product_id,
    )

    if not existing:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found.",
        )

    return ProductMasterRepository.delete(
        db,
        existing,
    )