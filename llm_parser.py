# llm_parser.py
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def parse_query_with_llm(query: str) -> dict:
    """
    Uses OpenAI GPT to parse a natural language insurance question into structured JSON.
    """
    prompt = f"""
    Extract the structured fields from the following insurance claim query:

    Query: "{query}"

    Return only a JSON with these fields:
    - age (int)
    - gender (Male/Female/Other)
    - procedure (string)
    - location (city name)
    - policy_age_months (int)

    Example output:
    {{
      "age": 46,
      "gender": "Male",
      "procedure": "knee surgery",
      "location": "Pune",
      "policy_age_months": 3
    }}
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    try:
        json_output = response.choices[0].message.content.strip()
        return eval(json_output)  # safer in real-world: use json.loads()
    except Exception as e:
        print(f"Error parsing output: {e}")
        return {"error": "Parsing failed"}
