from pydantic import BaseModel
from typing import Optional

class Quote(BaseModel):
    supplier_name: Optional[str]
    annual_quantity: Optional[float]
    unit_price: Optional[float]
    annual_price_total: Optional[float]
    currency: Optional[str]
    tooling_costs: Optional[float]
    delivery_terms: Optional[str]
    delivery_timeline_days: Optional[float]
    payment_terms: Optional[str]
    contract_conditions: Optional[str]