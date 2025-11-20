# 🧠 Intelligent Supplier Agent

## Problem
Procurement teams spend hours manually extracting and comparing supplier quotations from PDFs with inconsistent formats. This process is slow, error-prone, and difficult to scale.

## Solution
An AI-powered agent that:
- **Automatically extracts structured data** from supplier quotation PDFs (supplier name, price, quantity, tooling costs, delivery terms, conditions).
- **Performs multi-criteria comparison** across offers.
- **Recommends the best supplier** with clear reasoning.
- Uses **dual processing pipelines** for robust and reliable extraction.

---

## ⚙️ Setup
1. Get a Gemini API key from **Google AI Studio**.
2. Add your API key to a `.env` file:
   ```bash
   GEMINI_API_KEY=your_actual_api_key

Install dependencies:

bash
pip install -r requirements.txt

🚀 Usage
AI Agent Pipeline (Recommended)

bash python main_crew.py


