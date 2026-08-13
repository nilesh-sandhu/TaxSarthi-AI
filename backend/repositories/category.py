from sqlalchemy.orm import Session

from models.category import Category
from schemas.category import (
    CategoryCreate,
    CategoryUpdate,
)


class CategoryRepository:

    # =====================================================
    # Create Category
    # =====================================================

    @staticmethod
    def create(
        db: Session,
        category: CategoryCreate,
    ):

        new_category = Category(
            **category.model_dump()
        )

        db.add(new_category)

        db.commit()

        db.refresh(new_category)

        return new_category

    # =====================================================
    # Get All Categories
    # =====================================================

    @staticmethod
    def get_all(db: Session):

        return (
            db.query(Category)
            .order_by(Category.name.asc())
            .all()
        )

    # =====================================================
    # Get Category By ID
    # =====================================================

    @staticmethod
    def get_by_id(
        db: Session,
        category_id: int,
    ):

        return (
            db.query(Category)
            .filter(Category.id == category_id)
            .first()
        )

    # =====================================================
    # Get Category By Name
    # =====================================================

    @staticmethod
    def get_by_name(
        db: Session,
        name: str,
    ):

        return (
            db.query(Category)
            .filter(Category.name.ilike(name))
            .first()
        )

    # =====================================================
    # Search Categories
    # =====================================================

    @staticmethod
    def search(
        db: Session,
        keyword: str,
    ):

        return (
            db.query(Category)
            .filter(
                Category.name.ilike(
                    f"%{keyword}%"
                )
            )
            .all()
        )

    # =====================================================
    # Update Category
    # =====================================================

    @staticmethod
    def update(
        db: Session,
        category: Category,
        updated_data: CategoryUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                category,
                key,
                value,
            )

        db.commit()

        db.refresh(category)

        return category

    # =====================================================
    # Soft Delete
    # =====================================================

    @staticmethod
    def delete(
        db: Session,
        category: Category,
    ):

        category.is_active = False

        db.commit()

        db.refresh(category)

        return category