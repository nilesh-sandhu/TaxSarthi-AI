from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from repositories.gst_rule import GSTRuleRepository
from schemas.gst_rule import (
    GSTRuleCreate,
    GSTRuleUpdate,
)


def create_rule(
    rule: GSTRuleCreate,
    db: Session,
):

    existing = GSTRuleRepository.get_by_name(
        db,
        rule.rule_name,
    )

    if existing:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rule already exists.",
        )

    return GSTRuleRepository.create(
        db,
        rule,
    )


def get_rules(
    db: Session,
):

    return GSTRuleRepository.get_all(db)


def get_rule(
    rule_id: int,
    db: Session,
):

    rule = GSTRuleRepository.get_by_id(
        db,
        rule_id,
    )

    if not rule:

        raise HTTPException(
            status_code=404,
            detail="Rule not found.",
        )

    return rule


def update_rule(
    rule_id: int,
    rule: GSTRuleUpdate,
    db: Session,
):

    existing = GSTRuleRepository.get_by_id(
        db,
        rule_id,
    )

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Rule not found.",
        )

    return GSTRuleRepository.update(
        db,
        existing,
        rule,
    )


def delete_rule(
    rule_id: int,
    db: Session,
):

    existing = GSTRuleRepository.get_by_id(
        db,
        rule_id,
    )

    if not existing:

        raise HTTPException(
            status_code=404,
            detail="Rule not found.",
        )

    return GSTRuleRepository.delete(
        db,
        existing,
    )