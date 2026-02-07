"""Vector retriever using Pinecone (cosine similarity)."""

import os

from dotenv import load_dotenv
from pinecone import Pinecone

from ingest.embedding import embed_query

load_dotenv()


def search(query: str, top_k: int = 10) -> list[dict]:
    """Vector cosine similarity search.

    Args:
        query: Search query string.
        top_k: Number of results to return.

    Returns:
        list[dict], each dict has keys: "id", "text", "score", "method".
        "method" should be "Vector".

    Hints:
        - Use embed_query(query) to get the query embedding vector
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Use index.query(vector=..., top_k=..., include_metadata=True)
        - Text is in match["metadata"]["text"]
    """
    # TODO: Implement vector search
    qvec = embed_query(query)

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")
    if not api_key or not index_name:
        raise ValueError("PINECONE_API_KEY / PINECONE_INDEX not set.")

    pc = Pinecone(api_key=api_key)
    index = pc.Index(index_name)

    response = index.query(vector=qvec, top_k=top_k, include_metadata=True)

    matches = response.get("matches", []) if isinstance(response, dict) else getattr(response, "matches", [])
    result = []
    for m in matches:
        # pinecone may return dicts or objects depending on version
        if isinstance(m, dict):
            doc_id = m.get("id")
            score = m.get("score", 0.0)
            md = m.get("metadata", {}) or {}
            text = md.get("text", "")
        else:
            doc_id = getattr(m, "id", None)
            score = getattr(m, "score", 0.0)
            md = getattr(m, "metadata", {}) or {}
            text = md.get("text", "")

        result.append(
            {
                "id": doc_id,
                "text": text,
                "score": score,
                "method": "Vector",
            }
        )
        
    return result

