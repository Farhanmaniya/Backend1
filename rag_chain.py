# rag_chain.py

import os
import tempfile
import requests
import google.generativeai as genai
from PyPDF2 import PdfReader
from dotenv import load_dotenv

from langchain_community.vectorstores import FAISS
from langchain.embeddings import GoogleGenerativeAIEmbeddings
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# -----------------------------
# 🧩 1. Load PDF from URL
# -----------------------------
def load_pdf_from_url(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("❌ Failed to download PDF from URL.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# -----------------------------
# ✂️ 2. Chunk PDF into documents
# -----------------------------
def chunk_text(text: str):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([text])
    return chunks

# -----------------------------
# 🧠 3. Embed + Search + Answer
# -----------------------------
def get_answers(doc_url: str, questions: list[str], k: int = 3) -> list[str]:
    """
    Process a PDF and answer questions using Gemini + FAISS-based semantic search.

    Args:
        doc_url (str): Public PDF URL.
        questions (list[str]): List of user questions.
        k (int): Number of top chunks to retrieve.

    Returns:
        list[str]: Answers from Gemini based on semantic match.
    """

    # 1. Load and chunk the document
    raw_text = load_pdf_from_url(doc_url)
    documents = chunk_text(raw_text)

    # 2. Embed using Gemini's embedding model
    embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(documents, embedding)

    # 3. Gemini LLM
    llm = genai.GenerativeModel("models/gemini-1.5-pro")

    # 4. For each question → search → build prompt → get answer
    answers = []
    for question in questions:
        matched_docs = vectorstore.similarity_search(question, k=k)
        context = "\n".join(doc.page_content for doc in matched_docs)
        prompt = f"""
You are a helpful assistant. Use the below context extracted from a PDF to answer the question. Be concise and accurate.

Context:
{context}

Question: {question}
Answer:
"""
        response = llm.generate_content(prompt)
        answers.append(response.text.strip())

    return answers
