from core.database import SessionLocal
from models.category import Category


categories = [

    {
        "name": "Electronics",
        "description": "Electronic devices and accessories",
    },
    {
        "name": "Furniture",
        "description": "Home and office furniture",
    },
    {
        "name": "Food & Grocery",
        "description": "Food items and grocery products",
    },
    {
        "name": "Medical",
        "description": "Medicines and healthcare products",
    },
    {
        "name": "Agriculture",
        "description": "Agricultural products and equipment",
    },
    {
        "name": "Automobile",
        "description": "Vehicles and spare parts",
    },
    {
        "name": "Clothing",
        "description": "Garments and apparel",
    },
    {
        "name": "Restaurant",
        "description": "Food services and restaurants",
    },
    {
        "name": "Education",
        "description": "Educational products and services",
    },
    {
        "name": "Services",
        "description": "Professional and business services",
    },
]


def seed_categories():

    db = SessionLocal()

    inserted = 0
    skipped = 0

    try:

        for category in categories:

            existing = (
                db.query(Category)
                .filter(Category.name == category["name"])
                .first()
            )

            if existing:
                skipped += 1
                continue

            db.add(Category(**category))
            inserted += 1

        db.commit()

        print(f"✅ Inserted : {inserted}")
        print(f"⏭️ Skipped : {skipped}")

    finally:

        db.close()


if __name__ == "__main__":

    seed_categories()