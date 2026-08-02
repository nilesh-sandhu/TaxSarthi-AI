from sqlalchemy.orm import Session
from fastapi import HTTPException

from models.product import Product
from schemas.product import ProductCreate, ProductUpdate


# -----------------------------
# Create Product
# -----------------------------
def create_product(product: ProductCreate, db: Session):

    existing_product = db.query(Product).filter(
        Product.name == product.name
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail="Product already exists."
        )

    new_product = Product(
        name=product.name,
        category=product.category,
        gst_rate=product.gst_rate,
        hsn_code=product.hsn_code,
        description=product.description
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


# -----------------------------
# Get All Products
# -----------------------------
def get_products(db: Session):

    return db.query(Product).all()


# -----------------------------
# Get Product By ID
# -----------------------------
def get_product(product_id: int, db: Session):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product


# -----------------------------
# Update Product
# -----------------------------
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session,
):

    existing = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    existing.name = product.name
    existing.category = product.category
    existing.gst_rate = product.gst_rate
    existing.hsn_code = product.hsn_code
    existing.description = product.description

    db.commit()
    db.refresh(existing)

    return existing


# -----------------------------
# Delete Product
# -----------------------------
def delete_product(product_id: int, db: Session):

    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    db.delete(product)
    db.commit()

    return {
        "message": "Product deleted successfully."
    }
# -----------------------------
# Search Product
# -----------------------------
def search_product(name: str, db: Session):

    product = (
        db.query(Product)
        .filter(Product.name.ilike(f"%{name}%"))
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Product not found."
        )

    return product