import pandas as pd
from models_generic import ComparisonOutput
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def comparison_to_dataframe(comp: ComparisonOutput) -> pd.DataFrame:
    return pd.DataFrame([row.model_dump() for row in comp.rows])

def export_comparison(comp: ComparisonOutput, base_filename: str = "supplier_comparison"):
    df = comparison_to_dataframe(comp)
    
    if df.empty:
        print("No data to export - comparison returned empty results")
        return
    
    # Export CSV only
    df.to_csv(f"{base_filename}.csv", index=False)
    print(f"Exported: {base_filename}.csv")