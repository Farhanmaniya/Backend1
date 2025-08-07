# llm_parser.py
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-pro")

def parse_query_with_llm(query: str) -> dict:
    """
    Uses Gemini to parse a natural language insurance query into structured JSON.
    """
    prompt = f"""
You are a helpful assistant that extracts structured fields from insurance claim queries.

Extract the following from the user query:
- age (int)
- gender (Male/Female/Other)
- procedure (string)
- location (city name)
- policy_age_months (int)

Return only valid JSON format, without any explanation.

Query: "{query}"

Expected Output Example:
{{
  "age": 46,
  "gender": "Male",
  "procedure": "knee surgery",
  "location": "Pune",
  "policy_age_months": 3
}}
"""

    try:
        response = model.generate_content(prompt)
        return eval(response.text.strip())  # ✅ For prototyping; use json.loads() in production
    except Exception as e:
        print(f"Error parsing output: {e}")
        return {"error": "Parsing failed"}
