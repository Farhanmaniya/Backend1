# qa_utils.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

from pdf_utils import download_pdf, extract_text_from_pdf

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-flash")


def get_answers_from_pdf(pdf_url: str, questions: list) -> list:
    """
    Downloads a PDF, extracts text, and uses Gemini to answer the provided questions.
    
    Args:
        pdf_url (str): Public URL of the PDF.
        questions (list): List of natural language questions.
    
    Returns:
        list: Cleaned answers returned by Gemini.
    """
    # Download and extract content
    pdf_path = download_pdf(pdf_url)
    text = extract_text_from_pdf(pdf_path)

    # Build the prompt for Gemini
    prompt = f"""You are a document-question-answering AI assistant.
Use the following content from a PDF to answer specific questions.
Do not assume or hallucinate. Only use what's present in the PDF.

--- PDF Content ---
{text}
-------------------

Answer the following questions:
"""

    for i, q in enumerate(questions, 1):
        prompt += f"\nQ{i}: {q}"

    # Call Gemini model
    response = model.generate_content(prompt)

    # Clean and split answers
    raw_output = response.text.strip().split("\n")
    cleaned = [a.split(":", 1)[-1].strip() if ":" in a else a.strip() for a in raw_output]
    return cleaned
