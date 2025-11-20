import os
import json
import re
from models import Quote

def extract_quote(raw_text: str) -> Quote:
    # Extract supplier name - look for various patterns
    supplier_patterns = [
        r'Supplier[:]*\s*([A-Za-z0-9_\s&.,()-]+?)\n',
        r'From[:]*\s*([A-Za-z0-9_\s&.,()-]+?)\n',
        r'Company[:]*\s*([A-Za-z0-9_\s&.,()-]+?)\n',
        r'([A-Za-z0-9_]+_[A-Za-z0-9_]+)',  # Pattern like TG_Display_Japan
        r'Customer[:]*\s*([A-Za-z0-9_\s&.,()-]+?)\n'
    ]
    
    supplier_name = None
    for pattern in supplier_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            supplier_name = match.group(1).strip()
            break
    
    # Look for quantities - improved patterns
    qty_patterns = [
        r'Volume[:]*\s*([0-9,.]+)',
        r'Annual.*?Volume.*?([0-9,.]+)',
        r'Quantity[:]*\s*([0-9,.]+)',
        r'([0-9,.]+)\s*pcs'
    ]
    
    annual_quantity = None
    for pattern in qty_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            annual_quantity = float(match.group(1).replace(',', '').replace('.', ''))
            break
    
    # Look for unit prices - improved patterns
    price_patterns = [
        r'Price[:]*\s*([0-9.,]+)\s*USD',
        r'([0-9.,]+)\s*USD',
        r'Unit.*?Price[:]*\s*([0-9.,]+)',
        r'Price[:]*\s*([0-9.,]+)'
    ]
    
    unit_price = None
    for pattern in price_patterns:
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if match:
            unit_price = float(match.group(1).replace(',', ''))
            break
    
    # Look for currency
    currency_match = re.search(r'\b(USD|EUR|GBP|JPY|CNY)\b', raw_text, re.IGNORECASE)
    currency = currency_match.group(1).upper() if currency_match else None
    
    # Look for tooling costs
    tooling_match = re.search(r'(?:tooling|nre|setup).*?([0-9.,]+)', raw_text, re.IGNORECASE)
    tooling_costs = float(tooling_match.group(1).replace(',', '')) if tooling_match else 0.0
    
    # Calculate annual total if possible
    annual_price_total = None
    if annual_quantity and unit_price:
        annual_price_total = annual_quantity * unit_price
    
    print(f"Extracted: {supplier_name}, qty={annual_quantity}, price={unit_price}, currency={currency}")
    
    return Quote(
        supplier_name=supplier_name,
        annual_quantity=annual_quantity,
        unit_price=unit_price,
        annual_price_total=annual_price_total,
        currency=currency,
        tooling_costs=tooling_costs,
        delivery_terms=None,
        delivery_timeline_days=None,
        payment_terms=None,
        contract_conditions=None
    )