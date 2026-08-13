import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from core.database import SessionLocal
from engines.gst_engine import product_gst


def test_product_gst_laptop_db():
    db = SessionLocal()
    try:
        res = product_gst('Laptop', amount=1000, interstate=False, db=db)
        assert res.get('success') is True
        assert res.get('source') == 'product_master'
        assert float(res.get('gst_rate', 0)) == 18.0
    finally:
        db.close()


def test_product_gst_tea_db():
    db = SessionLocal()
    try:
        res = product_gst('Tea', amount=1000, interstate=False, db=db)
        assert res.get('success') is True
        assert res.get('source') == 'knowledge_base'
        assert float(res.get('gst_rate', 0)) == 5.0
    finally:
        db.close()
