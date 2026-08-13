from sqlalchemy.orm import Session

from models.product_alias import ProductAlias
from models.product_master import ProductMaster


def seed_product_alias(db: Session):

    aliases = {
        "Laptop": [
            "Notebook",
            "Laptop Computer",
            "Dell Laptop",
            "HP Laptop",
            "Lenovo Laptop",
            "MacBook",
        ],
        "Mobile Phone": [
            "Phone",
            "Smartphone",
            "Cell Phone",
            "Android Phone",
            "iPhone",
        ],
        "Television": [
            "TV",
            "Smart TV",
            "LED TV",
            "OLED TV",
        ],
        "Refrigerator": [
            "Fridge",
            "Double Door Fridge",
        ],
    }

    for product_name, alias_list in aliases.items():

        product = (
            db.query(ProductMaster)
            .filter(
                ProductMaster.product_name == product_name
            )
            .first()
        )

        if not product:
            continue

        for alias in alias_list:

            exists = (
                db.query(ProductAlias)
                .filter(
                    ProductAlias.alias == alias
                )
                .first()
            )

            if exists:
                continue

            db.add(
                ProductAlias(
                    product_id=product.id,
                    alias=alias,
                )
            )

    db.commit()

    print("✅ Product Alias Seed Completed")