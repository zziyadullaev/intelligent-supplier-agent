import os
from dotenv import load_dotenv
from pdf_processor import pdf_to_text
from crew_generic import run_generic_analysis
from export_utils import export_comparison

load_dotenv()

def process_quotes_generic(pdf_paths: list, scenario: dict = None) -> None:
    from datetime import datetime
    
    for i, pdf_path in enumerate(pdf_paths, 1):
        print(f"\n=== Processing PDF {i}/{len(pdf_paths)}: {pdf_path} ===")
        text = pdf_to_text(pdf_path)
        print(f"Extracted {len(text)} characters")
        
        print(f"Running analysis for {pdf_path}...")
        comparison = run_generic_analysis([text], scenario)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_name = pdf_path.split('/')[-1].replace('.pdf', '')
        
        if comparison and hasattr(comparison, 'rows'):
            print(f"Found {len(comparison.rows)} suppliers")
            for row in comparison.rows:
                print(f"- {row.supplier_name}: ${row.tco_usd:,.0f} TCO")
            
            # Export with PDF-specific filename
            pdf_name_clean = pdf_name.replace('\\', '_').replace('/', '_')
        comparison_filename = f"analysis_{pdf_name_clean}_{timestamp}"
            export_comparison(comparison, comparison_filename)
            print(f"Exported: {comparison_filename}.*")
        else:
            print("Analysis completed but no structured output generated")
    
    print("\n=== All PDFs processed ===")

if __name__ == "__main__":
    import glob
    pdf_files = glob.glob("pdf_files/*.pdf")
    
    scenario = {
        "target_currency": "USD",
        "horizon_years": None,
        "description": "All available years with pricing data"
    }
    
    process_quotes_generic(pdf_files, scenario)