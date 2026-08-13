import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
from engines.gst_engine import normalize_text, clean_product_name, calculate_tax


def test_normalize_text():
    assert normalize_text('  T-Shirt  ') == 't shirt'
    assert normalize_text('Tshirts') == 't shirt'


def test_clean_product_name():
    assert clean_product_name('What is the GST on Laptop?') == 'laptop?'
    assert clean_product_name('gst rate for Tea') == 'tea'


def test_calculate_tax_intrastate():
    tax = calculate_tax(1000, 18, interstate=False)
    assert tax['cgst'] == 90.0
    assert tax['sgst'] == 90.0
    assert tax['igst'] == 0


def test_calculate_tax_interstate():
    tax = calculate_tax(1000, 18, interstate=True)
    assert tax['cgst'] == 0
    assert tax['sgst'] == 0
    assert tax['igst'] == 180.0
