# pdf_utils.py
import requests
import fitz  # PyMuPDF
import tempfile

def download_pdf(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.write(response.content)
    temp.close()
    return temp.name

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text.strip()
