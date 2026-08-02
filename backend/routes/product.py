from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
)

from services.product import (
    create_product,
    get_products,
    get_product,
    update_product,
    delete_product,
    search_product,
)

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


# -----------------------------
# Create Product
# -----------------------------
@router.post("/", response_model=ProductResponse)
def add_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    return create_product(product, db)


# -----------------------------
# Get All Products
# -----------------------------
@router.get("/", response_model=list[ProductResponse])
def all_products(
    db: Session = Depends(get_db),
):
    return get_products(db)


# -----------------------------
# Search Product By Name
# -----------------------------
@router.get(
    "/search/{name}",
    response_model=ProductResponse,
)
def find_product(
    name: str,
    db: Session = Depends(get_db),
):
    return search_product(name, db)


# -----------------------------
# Get Product By ID
# -----------------------------
@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def single_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return get_product(product_id, db)


# -----------------------------
# Update Product
# -----------------------------
@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def edit_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
):
    return update_product(product_id, product, db)


# -----------------------------
# Delete Product
# -----------------------------
@router.delete("/{product_id}")
def remove_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    return delete_product(product_id, db)