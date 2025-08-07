from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv
from qa_utils import get_answers_from_pdf

load_dotenv()
app = FastAPI()

API_KEY = os.getenv("API_KEY")  # Bearer token

class HackRxRequest(BaseModel):
    documents: str
    questions: List[str]

@app.post("/hackrx/run")  # ✅ MUST BE EXACT
async def run_hackrx(request: Request, body: HackRxRequest):
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        answers = get_answers_from_pdf(body.documents, body.questions)
        return JSONResponse(content={"answers": answers}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/")
def home():
    return {"message": "Backend is running!"}
