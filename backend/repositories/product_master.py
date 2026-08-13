from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.product_master import ProductMaster
from schemas.product_master import (
    ProductMasterCreate,
    ProductMasterUpdate,
)


class ProductMasterRepository:

    # =====================================================
    # Create Product
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        product: ProductMasterCreate,
    ):

        new_product = ProductMaster(
            **product.model_dump()
        )

        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product

    # =====================================================
    # Get All Products
    # =====================================================

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(ProductMaster)
            .filter(ProductMaster.is_active == True)
            .order_by(ProductMaster.product_name.asc())
            .all()
        )

    # =====================================================
    # Get Product By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        product_id: int,
    ):

        return (
            db.query(ProductMaster)
            .filter(
                ProductMaster.id == product_id,
                ProductMaster.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Get Product By Name
    # =====================================================

    @staticmethod
    def get_by_name(
        db: Session,
        product_name: str,
    ):

        return (
            db.query(ProductMaster)
            .filter(
                ProductMaster.product_name.ilike(product_name),
                ProductMaster.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Search Product
    # =====================================================

    @staticmethod
    def search(
        db: Session,
        keyword: str,
    ):

        return (
            db.query(ProductMaster)
            .filter(
                ProductMaster.is_active == True
            )
            .filter(
                or_(
                    ProductMaster.product_name.ilike(f"%{keyword}%"),
                    ProductMaster.description.ilike(f"%{keyword}%"),
                )
            )
            .order_by(ProductMaster.product_name.asc())
            .all()
        )

    # =====================================================
    # Update Product
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        product: ProductMaster,
        updated_data: ProductMasterUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                product,
                key,
                value,
            )

        db.commit()
        db.refresh(product)

        return product

    # =====================================================
    # Soft Delete
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        product: ProductMaster,
    ):

        product.is_active = False

        db.commit()
        db.refresh(product)

        return product