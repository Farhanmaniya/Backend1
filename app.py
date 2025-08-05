# app.py
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os

from rag_chain import get_answers
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
app = FastAPI()

API_KEY = os.getenv("API_KEY")  # Securely loaded from .env

class HackRxRequest(BaseModel):
    documents: str
    questions: List[str]

@app.post("/hackrx/run")
async def run_hackrx(request: Request, body: HackRxRequest):
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        answers = get_answers(body.documents, body.questions)
        return JSONResponse(content={"answers": answers}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
