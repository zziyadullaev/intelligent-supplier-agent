import os
from crewai import Agent, Task, Crew, LLM, Process
from models_generic import QuotesBatch, ComparisonOutput

llm = LLM(
    model="gemini/gemini-2.5-flash",
    api_key=os.environ["GEMINI_API_KEY"],
    temperature=0.0,
)

extraction_agent = Agent(
    role="Supplier quotation extraction specialist",
    goal=(
        "Turn any supplier quotation PDF text into a JSON object that follows the Quote schema, "
        "without guessing numbers."
    ),
    backstory=(
        "You process many different supplier quotations with different formats and naming. "
        "You care about monetary accuracy and you never invent values that are not stated or "
        "clearly implied."
    ),
    llm=llm,
    verbose=True,
)

comparison_agent = Agent(
    role="Sourcing and TCO analysis specialist",
    goal=(
        "Turn generic quote JSON into a numeric comparison table and a recommendation "
        "that can be exported to CSV, Excel, and PDF."
    ),
    backstory=(
        "You handle many different supplier quotations. You can adapt to any mix of years, "
        "currencies and extras by applying a clear cost scenario and making all assumptions explicit."
    ),
    llm=llm,
    verbose=True,
)

extraction_task = Task(
    description=(
        "Extract essential supplier data from PDF texts. Process each text in {pdf_texts} and extract:\n"
        "- supplier_name: Company/supplier name\n"
        "- part_name: Product/part name\n"
        "- base_currency: Currency (USD, EUR, etc.)\n"
        "- yearly_prices: List with year, quantity, unit_price, currency\n"
        "- extras: Tooling costs, NRE, packaging (charge_type, amount, currency, basis)\n"
        "- delivery_terms: Shipping terms\n"
        "- lead_times: Delivery timelines (item, value, unit)\n"
        "- moq_pcs: Minimum order quantity\n"
        "Set missing fields to null. Extract only what's explicitly stated."
    ),
    expected_output="A JSON object with key 'quotes' that validates against the QuotesBatch model.",
    agent=extraction_agent,
    output_pydantic=QuotesBatch,
    markdown=False,
)

comparison_task = Task(
    description=(
        "You receive two inputs:\n"
        "- `quotes`: a list of Quote objects extracted from PDFs.\n"
        "- `scenario`: an object with fields:\n"
        "   * target_currency: 3-letter code to report TCO in (e.g., 'USD').\n"
        "   * horizon_years: optional list of integers; if present, only use these years. "
        "     If missing, use all distinct years that have prices.\n"
        "   * description: free text scenario description.\n\n"
        "Your job:\n"
        "1) For each supplier, choose the yearly price lines that fall inside horizon_years "
        "(or all years if horizon_years is null). If a yearly line has no numeric year but "
        "the label clearly implies order, treat them as consecutive years and include them.\n"
        "2) Compute total_volume_pcs, parts_cost_native, parts_cost_usd, extras_cost_usd, tco_usd, "
        "and avg_tco_per_pc_usd using the target currency.\n"
        "3) Build SupplierSummaryRow objects for each supplier with all required fields.\n"
        "4) Sort rows by tco_usd ascending.\n"
        "5) Compose recommendation_markdown that explains which supplier is best and why, "
        "including percentage differences and risk flags.\n\n"
        "Return a JSON object that validates as ComparisonOutput."
    ),
    expected_output="A JSON object with keys 'rows' and 'recommendation_markdown' as ComparisonOutput.",
    agent=comparison_agent,
    output_pydantic=ComparisonOutput,
    markdown=False,
    context=[extraction_task],
)

def save_extracted_data(extraction_result, timestamp: str):
    """Save extracted quotes data to CSV"""
    import pandas as pd
    import os
    
    os.makedirs("data_extracted", exist_ok=True)
    
    if hasattr(extraction_result, 'quotes') and extraction_result.quotes:
        quotes_data = []
        for quote in extraction_result.quotes:
            row = {
                'supplier_name': quote.supplier_name,
                'part_name': quote.part_name,
                'base_currency': quote.base_currency,
                'moq_pcs': quote.moq_pcs,
                'delivery_terms': quote.delivery_terms,
                'yearly_prices_count': len(quote.yearly_prices) if quote.yearly_prices else 0,
                'extras_count': len(quote.extras) if quote.extras else 0
            }
            quotes_data.append(row)
        
        df = pd.DataFrame(quotes_data)
        csv_filename = f"data_extracted/quotes_extracted_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Extracted data saved to: {csv_filename}")
        return csv_filename
    return None

def run_generic_analysis(pdf_texts: list, scenario: dict = None) -> ComparisonOutput:
    if scenario is None:
        scenario = {
            "target_currency": "USD",
            "horizon_years": None,
            "description": "Default: all years with explicit prices"
        }
    crew = Crew(
        agents=[extraction_agent, comparison_agent],
        tasks=[extraction_task, comparison_task],
        process=Process.sequential,
        verbose=True,
    )
    result = crew.kickoff(inputs={"pdf_texts": pdf_texts, "scenario": scenario})
    
    # Save extraction data (raw output if Pydantic fails)
    from datetime import datetime
    import json
    import os
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if len(result.tasks_output) > 0:
        extraction_output = result.tasks_output[0]
        if hasattr(extraction_output, 'pydantic') and extraction_output.pydantic:
            save_extracted_data(extraction_output.pydantic, timestamp)
        else:
            # Save raw output as JSON
            os.makedirs("data_extracted", exist_ok=True)
            raw_filename = f"data_extracted/raw_extraction_{timestamp}.json"
            with open(raw_filename, 'w') as f:
                json.dump({"raw_output": str(extraction_output.raw)}, f, indent=2)
            print(f"Raw extraction saved to: {raw_filename}")
    
    return result.tasks_output[-1].pydantic if len(result.tasks_output) > 1 else None