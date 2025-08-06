# qa_utils.py
import google.generativeai as genai
import os

from pdf_utils import download_pdf, extract_text_from_pdf
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_answers_from_pdf(pdf_url: str, questions: list) -> list:
    pdf_path = download_pdf(pdf_url)
    text = extract_text_from_pdf(pdf_path)

    prompt = f"""You are a document question answering AI. Use the following PDF content to answer questions.

PDF Content:
{text}

Answer the following questions based only on the document:
"""
    for i, q in enumerate(questions, 1):
        prompt += f"\nQ{i}: {q}"

    response = model.generate_content(prompt)
    
    # Split answers cleanly if AI returns all in one chunk
    answers = response.text.strip().split("\n")
    cleaned = [a.split(":", 1)[-1].strip() if ":" in a else a.strip() for a in answers]
    return cleaned
