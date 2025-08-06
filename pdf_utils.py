import requests
from io import BytesIO
from pdfminer.high_level import extract_text

def download_pdf(pdf_url: str) -> BytesIO:
    response = requests.get(pdf_url)
    response.raise_for_status()
    return BytesIO(response.content)

def extract_text_from_pdf(pdf_file: BytesIO) -> str:
    text = extract_text(pdf_file)
    return text
