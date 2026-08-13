from sqlalchemy.orm import Session

from models.product_alias import ProductAlias
from schemas.product_alias import (
    ProductAliasCreate,
    ProductAliasUpdate,
)


class ProductAliasRepository:

    # =====================================================
    # Create Alias
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        alias: ProductAliasCreate,
    ):

        new_alias = ProductAlias(
            **alias.model_dump()
        )

        db.add(new_alias)

        db.commit()

        db.refresh(new_alias)

        return new_alias

    # =====================================================
    # Get All Aliases
    # =====================================================

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(ProductAlias)
            .filter(
                ProductAlias.is_active == True
            )
            .order_by(
                ProductAlias.alias.asc()
            )
            .all()
        )

    # =====================================================
    # Get Alias By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        alias_id: int,
    ):

        return (
            db.query(ProductAlias)
            .filter(
                ProductAlias.id == alias_id,
                ProductAlias.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Get Alias
    # =====================================================

    @staticmethod
    def get_by_alias(
        db: Session,
        alias: str,
    ):

        return (
            db.query(ProductAlias)
            .filter(
                ProductAlias.alias.ilike(alias),
                ProductAlias.is_active == True,
            )
            .first()
        )

    # =====================================================
    # Search Alias
    # =====================================================

    @staticmethod
    def search(
        db: Session,
        keyword: str,
    ):

        return (
            db.query(ProductAlias)
            .filter(
                ProductAlias.is_active == True,
                ProductAlias.alias.ilike(
                    f"%{keyword}%"
                ),
            )
            .all()
        )

    # =====================================================
    # Update Alias
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        alias: ProductAlias,
        updated_data: ProductAliasUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                alias,
                key,
                value,
            )

        db.commit()

        db.refresh(alias)

        return alias

    # =====================================================
    # Soft Delete
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        alias: ProductAlias,
    ):

        alias.is_active = False

        db.commit()

        db.refresh(alias)

        return alias