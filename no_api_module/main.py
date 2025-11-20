import os
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pdf_processor import pdf_to_text
from normalizer import normalize_all
from comparator import quotes_to_table

load_dotenv()

# Import after loading env
from extractor import extract_quote

def process_quotes(pdf_paths: list) -> None:
    quotes = []
    
    for pdf_path in pdf_paths:
        print(f"Processing {pdf_path}...")
        text = pdf_to_text(pdf_path)
        quote = extract_quote(text)
        quotes.append(quote)
    
    normalized_quotes = normalize_all(quotes)
    comparison_table = quotes_to_table(normalized_quotes)
    
    print("\nComparison Table:")
    print(comparison_table.to_string(index=False))
    
    # Save to CSV
    comparison_table.to_csv("quote_comparison.csv", index=False)
    print("\nResults saved to quote_comparison.csv")

if __name__ == "__main__":
    import glob
    pdf_files = glob.glob("../pdf_files/*.pdf")
    print(f"Found {len(pdf_files)} PDF files: {pdf_files}")
    process_quotes(pdf_files)