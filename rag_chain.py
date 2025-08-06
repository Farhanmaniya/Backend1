# rag_chain.py

import google.generativeai as genai
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
import tempfile
import requests

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load PDF from remote URL
def load_pdf_from_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download PDF")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# Chunk PDF text
def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([text])
    return chunks

# Embed + search + respond
def get_answers(doc_url: str, questions: list[str]) -> list[str]:
    # 1. Load and chunk PDF
    text = load_pdf_from_url(doc_url)
    documents = chunk_text(text)

    # 2. Embedding with Gemini's model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents, embedding)

    # 3. Initialize Gemini LLM
    llm = genai.GenerativeModel(model_name="models/gemini-1.5-pro")

    answers = []
    for question in questions:
        docs = vectorstore.similarity_search(question, k=3)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"
        response = llm.generate_content(prompt)
        answers.append(response.text.strip())

    return answers
