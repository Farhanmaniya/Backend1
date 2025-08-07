# logic_evaluator.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

def evaluate_clause_with_llm(question: str, clause: str) -> dict:
    prompt = f"""
You are an expert policy evaluator for insurance documents.

Given:
- User Question: "{question}"
- Matching Clause: "{clause}"

Your job is to return a JSON object with:
- "decision": "Approved" or "Rejected" or "Not Clear"
- "amount": Specific amount or limit mentioned (if any), otherwise "N/A"
- "justification": Short explanation why this clause leads to this decision

Output format:
{{
  "decision": "...",
  "amount": "...",
  "justification": "..."
}}
"""
    response = model.generate_content(prompt)
    return safe_json_parse(response.text)


def safe_json_parse(text: str) -> dict:
    import json
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Fallback: try to extract manually
        lines = text.strip().splitlines()
        result = {"decision": "Not Clear", "amount": "N/A", "justification": "Unable to parse response properly."}
        for line in lines:
            if "decision" in line.lower():
                result["decision"] = line.split(":")[-1].strip()
            elif "amount" in line.lower():
                result["amount"] = line.split(":")[-1].strip()
            elif "justification" in line.lower():
                result["justification"] = line.split(":", 1)[-1].strip()
        return result
