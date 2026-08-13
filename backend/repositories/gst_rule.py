from sqlalchemy.orm import Session

from models.gst_rule import GSTRule
from schemas.gst_rule import (
    GSTRuleCreate,
    GSTRuleUpdate,
)


class GSTRuleRepository:

    @staticmethod
    def create(
        db: Session,
        rule: GSTRuleCreate,
    ):

        obj = GSTRule(
            **rule.model_dump()
        )

        db.add(obj)

        db.commit()

        db.refresh(obj)

        return obj

    @staticmethod
    def get_all(
        db: Session,
    ):

        return (
            db.query(GSTRule)
            .filter(GSTRule.is_active == True)
            .order_by(GSTRule.rule_name.asc())
            .all()
        )

    @staticmethod
    def get_by_id(
        db: Session,
        rule_id: int,
    ):

        return (
            db.query(GSTRule)
            .filter(
                GSTRule.id == rule_id,
                GSTRule.is_active == True,
            )
            .first()
        )

    @staticmethod
    def get_by_name(
        db: Session,
        name: str,
    ):

        return (
            db.query(GSTRule)
            .filter(
                GSTRule.rule_name == name,
                GSTRule.is_active == True,
            )
            .first()
        )

    @staticmethod
    def update(
        db: Session,
        rule: GSTRule,
        updated_data: GSTRuleUpdate,
    ):

        data = updated_data.model_dump(
            exclude_unset=True
        )

        for key, value in data.items():

            setattr(
                rule,
                key,
                value,
            )

        db.commit()

        db.refresh(rule)

        return rule

    @staticmethod
    def delete(
        db: Session,
        rule: GSTRule,
    ):

        rule.is_active = False

        db.commit()

        db.refresh(rule)

        return rule