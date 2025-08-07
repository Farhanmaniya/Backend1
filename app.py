from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()
API_KEY = os.getenv("API_KEY")  # Your API key from .env

# Initialize app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use ["https://your-frontend.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Models -----
class HackRxRequest(BaseModel):
    documents: str  # PDF URL
    questions: List[str]

# ----- Imports for pipeline -----
from llm_parser import parse_query_with_llm
from qa_utils import get_answers_from_pdf


# ----- Endpoints -----

@app.get("/")
def home():
    return {"message": "Backend is running!"}


@app.post("/parse_query")
async def parse_query(request: Request):
    body = await request.json()
    query = body.get("query")
    if not query:
        raise HTTPException(status_code=400, detail="Missing query")

    structured = parse_query_with_llm(query)
    return JSONResponse(content={"parsed": structured})


@app.post("/hackrx/run")
async def run_hackrx(request: Request, body: HackRxRequest):
    # --- Token Authentication ---
    auth = request.headers.get("Authorization")
    if not auth or auth != f"Bearer {API_KEY}":
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        # --- Core PDF QA pipeline ---
        answers = get_answers_from_pdf(body.documents, body.questions)
        return JSONResponse(content={"answers": answers}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
