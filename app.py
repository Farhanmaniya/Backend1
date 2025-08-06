from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

from qa_utils import get_answers_from_pdf

# Load .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Get API key from environment
API_KEY = os.getenv("API_KEY")  # Set this key in Render Dashboard -> Environment


# Pydantic model for request body
class HackRxRequest(BaseModel):
    documents: str
    questions: List[str]


# Root POST endpoint (Render calls POST /)
@app.post("/")
async def run_hackrx(request: Request, body: HackRxRequest):
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        answers = get_answers_from_pdf(body.documents, body.questions)
        return JSONResponse(content={"answers": answers}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


# Optional: GET endpoint for health check
@app.get("/")
def home():
    return {"message": "HackRx backend is live!"}
