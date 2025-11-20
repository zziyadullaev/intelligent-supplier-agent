from pydantic import BaseModel
from typing import Optional, List, Literal

class YearlyPrice(BaseModel):
    label: str
    year: Optional[int]
    quantity: Optional[int]
    unit_price: Optional[float]
    currency: Optional[str]

class ExtraCharge(BaseModel):
    charge_type: Literal["tooling", "nre", "packaging", "surcharge", "other"]
    description: str
    amount: Optional[float]
    currency: Optional[str]
    basis: Optional[Literal["one_time", "per_unit", "per_batch", "per_year", "unknown"]]

class LeadTime(BaseModel):
    item: Literal["parts", "tooling", "raw_material", "other"]
    value: Optional[float]
    unit: Literal["weeks", "days"]

class Quote(BaseModel):
    supplier_name: Optional[str]
    customer_name: Optional[str]
    part_name: Optional[str]
    base_currency: Optional[str]
    moq_pcs: Optional[int]
    yearly_prices: List[YearlyPrice]
    extras: List[ExtraCharge]
    delivery_terms: Optional[str]
    lead_times: List[LeadTime]
    payment_terms_parts: Optional[str]
    payment_terms_tooling: Optional[str]
    validity_days: Optional[int]
    packaging_included_flag: Optional[bool]
    exchange_rates_notes: Optional[str]
    notes: Optional[str]

class QuotesBatch(BaseModel):
    quotes: List[Quote]

class SupplierSummaryRow(BaseModel):
    supplier_name: str
    base_currency: str
    horizon_label: str
    years_covered: List[int]
    total_volume_pcs: int
    parts_cost_native: float
    parts_cost_usd: float
    extras_cost_usd: float
    tco_usd: float
    avg_tco_per_pc_usd: float
    lead_time_summary: str
    moq_pcs: Optional[int]
    delivery_terms: Optional[str]
    payment_terms_parts: Optional[str]
    packaging_in_price: str
    risk_flags: List[str]

class ComparisonOutput(BaseModel):
    rows: List[SupplierSummaryRow]
    recommendation_markdown: str