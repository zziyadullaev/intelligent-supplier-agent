import pandas as pd
from typing import List
from models import Quote

def quotes_to_table(quotes: List[Quote]) -> pd.DataFrame:
    rows = []
    for q in quotes:
        annual_cost = q.annual_price_total or 0.0
        tooling = q.tooling_costs or 0.0
        tco = annual_cost + tooling
        rows.append({
            "Supplier": q.supplier_name,
            "Annual quantity": q.annual_quantity,
            "Unit price": q.unit_price,
            "Annual price total": annual_cost,
            "Tooling costs": tooling,
            "Currency": q.currency,
            "Delivery terms": q.delivery_terms,
            "Delivery timeline (days)": q.delivery_timeline_days,
            "Payment terms": q.payment_terms,
            "TCO": tco,
        })
    df = pd.DataFrame(rows)
    if df.empty or "TCO" not in df.columns:
        return df
    return df.sort_values("TCO", ascending=True)