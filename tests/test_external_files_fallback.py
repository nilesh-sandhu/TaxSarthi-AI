import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

import pytest
from engines.gst_engine import product_gst
from core.database import SessionLocal


def test_external_files_fallback():
    db = SessionLocal()
    try:
        res = product_gst('Laptop', amount=1000, interstate=False, db=db)

        assert isinstance(res, dict)
        # Either DB or knowledge_base or external_files should provide a success result
        assert 'success' in res

        if res.get('success'):
            assert 'gst_rate' in res
            assert isinstance(res.get('gst_rate'), (int, float))
    finally:
        db.close()
