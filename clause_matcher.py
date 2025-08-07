# clause_matcher.py

from typing import List, Tuple
from sentence_transformers import SentenceTransformer, util

# Load model (same as used for embeddings)
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def rank_clauses_by_similarity(question: str, clauses: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
    """
    Ranks document clauses based on semantic similarity to a given question.

    Args:
        question (str): User question.
        clauses (List[str]): Candidate clauses to rank.
        top_k (int): Number of top results to return.

    Returns:
        List of tuples: (clause, score) sorted by relevance.
    """
    # Encode question and clause candidates
    q_embed = model.encode(question, convert_to_tensor=True)
    clause_embeds = model.encode(clauses, convert_to_tensor=True)

    # Compute cosine similarities
    similarities = util.cos_sim(q_embed, clause_embeds)[0]

    # Pair clause with similarity score
    ranked = list(zip(clauses, similarities.tolist()))

    # Sort by similarity, descending
    ranked.sort(key=lambda x: x[1], reverse=True)

    return ranked[:top_k]
