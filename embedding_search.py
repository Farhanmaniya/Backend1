# embedding_search.py

import faiss
import os
from sentence_transformers import SentenceTransformer
from qa_utils import extract_text_from_pdf  # existing function
import numpy as np

model = SentenceTransformer('all-MiniLM-L6-v2')  # 🔥 Fast & effective
DIM = 384  # Embedding size for MiniLM

def chunk_text(text, max_words=100):
    """
    Splits text into chunks of ~max_words
    """
    words = text.split()
    chunks = [" ".join(words[i:i+max_words]) for i in range(0, len(words), max_words)]
    return chunks

def create_faiss_index_from_pdf(pdf_url):
    """
    Extracts text from PDF → chunks → embeddings → FAISS index
    """
    raw_text = extract_text_from_pdf(pdf_url)
    chunks = chunk_text(raw_text)

    embeddings = model.encode(chunks, convert_to_numpy=True)
    index = faiss.IndexFlatL2(DIM)
    index.add(np.array(embeddings))

    return index, chunks  # return chunks for retrieval mapping

def search_top_chunks(index, chunks, query, top_k=3):
    """
    Finds top-k relevant chunks for the query using semantic similarity.
    """
    query_vec = model.encode([query], convert_to_numpy=True)
    D, I = index.search(np.array(query_vec), top_k)
    results = [chunks[i] for i in I[0]]
    return results
