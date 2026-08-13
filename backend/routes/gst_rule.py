from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from core.database import get_db

from schemas.gst_rule import (
    GSTRuleCreate,
    GSTRuleUpdate,
    GSTRuleResponse,
)

from services.gst_rule import (
    create_rule,
    get_rules,
    get_rule,
    update_rule,
    delete_rule,
)

router = APIRouter(
    prefix="/gst-rules",
    tags=["GST Rules"],
)


@router.post("/", response_model=GSTRuleResponse, status_code=201)
def add_rule(
    rule: GSTRuleCreate,
    db: Session = Depends(get_db),
):
    return create_rule(rule, db)


@router.get("/", response_model=list[GSTRuleResponse])
def all_rules(
    db: Session = Depends(get_db),
):
    return get_rules(db)


@router.get("/{rule_id}", response_model=GSTRuleResponse)
def single_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    return get_rule(rule_id, db)


@router.put("/{rule_id}", response_model=GSTRuleResponse)
def edit_rule(
    rule_id: int,
    rule: GSTRuleUpdate,
    db: Session = Depends(get_db),
):
    return update_rule(rule_id, rule, db)


@router.delete("/{rule_id}")
def remove_rule(
    rule_id: int,
    db: Session = Depends(get_db),
):
    return delete_rule(rule_id, db)