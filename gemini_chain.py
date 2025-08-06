# gemini_chain.py

import os
import requests
import google.generativeai as genai
from PyPDF2 import PdfReader
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Your Gemini API key

genai.configure(api_key=GEMINI_API_KEY)

def download_pdf(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download PDF")
    
    with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(response.content)
        return tmp_file.name

def extract_text_from_pdf(path: str) -> str:
    reader = PdfReader(path)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() or ""
    return full_text

def get_answers(document_url: str, questions: list[str]) -> list[str]:
    pdf_path = download_pdf(document_url)
    doc_text = extract_text_from_pdf(pdf_path)

    model = genai.GenerativeModel("gemini-pro")
    answers = []

    for question in questions:
        prompt = f"Answer the following question based on the document:\n\nDocument:\n{doc_text}\n\nQuestion: {question}"
        response = model.generate_content(prompt)
        answers.append(response.text.strip())

    return answers
