# Intelligent Supplier Agent

## Problem
Procurement teams spend hours manually extracting and comparing supplier quotations from PDFs with different formats.

## Solution
An AI agent that automatically extracts structured data from quotation PDFs (supplier name, price, quantity, tooling costs, delivery terms, conditions), performs multi-criteria comparison, and recommends the best offer with clear reasoning. Features robust and reliable extraction with dual processing pipelines.

## Setup

1. Get a Gemini API key from Google AI Studio
2. Add your API key to `.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### AI Agent Pipeline (Recommended)
```bash
python main_crew.py
```
**Features:**
- Processes any PDF format using 2 AI agents
- Extracts: supplier name, pricing, tooling costs, delivery terms, lead times
- Generates TCO analysis and recommendations
- Saves data to `data_extracted/quotes_extracted_TIMESTAMP.csv`
- Processes PDFs one-by-one for faster execution

### Simple Pipeline (Fallback)
```bash
cd no_api_module && python main.py
```
**Features:**
- Fast regex-based extraction
- Works without API calls
- Basic comparison table output

## Architecture

### Main Directory (AI Agents)
- `main_crew.py`: Entry point for AI pipeline
- `crew_generic.py`: 2 agents (extraction + comparison)
- `models_generic.py`: Flexible Pydantic schemas
- `export_utils.py`: CSV export functionality
- `pdf_processor.py`: PDF text extraction

### no_api_module/ (Simple Pipeline)
- `main.py`: Entry point for regex pipeline
- `extractor.py`: Pattern-based extraction
- `models.py`: Fixed schemas
- `normalizer.py` + `comparator.py`: Processing chain

## Output Files

- `data_extracted/quotes_extracted_YYYYMMDD_HHMMSS.csv` - Extracted supplier data
- `analysis_PDF_NAME_YYYYMMDD_HHMMSS.csv` - TCO comparison results"
