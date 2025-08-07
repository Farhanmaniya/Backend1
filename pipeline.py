import requests
from pdfminer.high_level import extract_text
from transformers import pipeline
import tempfile
from llm_parser import parse_query_with_llm
from logic_engine import evaluate_clause_with_llm
from semantic_search import get_top_matching_clauses


def download_pdf(url: str) -> str:
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download PDF.")

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp.write(response.content)
    tmp.close()
    return tmp.name


def extract_text_from_pdf(pdf_path: str) -> str:
    return extract_text(pdf_path)


def run_full_pipeline(documents: str, questions: list[str]) -> list[str]:
    pdf_path = download_pdf(documents)
    full_text = extract_text_from_pdf(pdf_path)

    results = []

    for question in questions:
        try:
            # Step 1: Extract top matching clauses from PDF text
            top_clauses = get_top_matching_clauses(question, full_text)

            if not top_clauses:
                results.append("No relevant clause found.")
                continue

            best_clause = top_clauses[0][0]  # Just the top match (text only)

            # Step 2: Evaluate clause using LLM
            eval_result = evaluate_clause_with_llm(question, best_clause)

            # Step 3: Format result to match HackRx expectations
            combined_answer = (
                f"{eval_result.get('decision', '')}. "
                f"{eval_result.get('justification', '')} "
                f"Amount: {eval_result.get('amount', 'N/A')}."
            )

            results.append(combined_answer.strip())
        except Exception as e:
            results.append(f"Error: {str(e)}")

    return results
