from datetime import date

from sqlalchemy.orm import Session

from models.gst_rule import GSTRule


def seed_gst_rules(db: Session):

    rules = [

        {
            "rule_name": "Registration Threshold (Goods)",
            "rule_value": "4000000",
            "description": "GST registration threshold for suppliers of goods.",
        },

        {
            "rule_name": "Registration Threshold (Services)",
            "rule_value": "2000000",
            "description": "GST registration threshold for service providers.",
        },

        {
            "rule_name": "Composition Scheme (Goods)",
            "rule_value": "15000000",
            "description": "Maximum turnover allowed under Composition Scheme for goods.",
        },

        {
            "rule_name": "Composition Scheme (Restaurant)",
            "rule_value": "5000000",
            "description": "Maximum turnover allowed under Composition Scheme for restaurants.",
        },

        {
            "rule_name": "Interstate Supply Registration",
            "rule_value": "Mandatory",
            "description": "GST registration is mandatory for interstate taxable supplies where applicable.",
        },

        {
            "rule_name": "E-Commerce Registration",
            "rule_value": "Mandatory",
            "description": "GST registration required for notified e-commerce sellers/operators.",
        },

    ]

    for item in rules:

        exists = (
            db.query(GSTRule)
            .filter(
                GSTRule.rule_name == item["rule_name"]
            )
            .first()
        )

        if exists:
            continue

        db.add(
            GSTRule(
                rule_name=item["rule_name"],
                rule_value=item["rule_value"],
                description=item["description"],
                effective_from=date.today(),
            )
        )

    db.commit()

    print("✅ GST Rules Seeded Successfully")