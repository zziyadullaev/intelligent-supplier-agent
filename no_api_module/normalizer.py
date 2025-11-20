from typing import List
from models import Quote

def normalize_quote(q: Quote) -> Quote:
    if q.currency:
        q.currency = q.currency.upper()
    if q.annual_price_total is None and q.unit_price is not None and q.annual_quantity is not None:
        q.annual_price_total = q.unit_price * q.annual_quantity
    if q.delivery_terms:
        q.delivery_terms = q.delivery_terms.strip()
    return q

def normalize_all(quotes: List[Quote]) -> List[Quote]:
    return [normalize_quote(q) for q in quotes]