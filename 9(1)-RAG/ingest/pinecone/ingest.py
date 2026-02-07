"""Ingest embeddings into Pinecone vector index.

Batch upsert: 100 vectors per call.
Metadata: text truncated to 1000 chars (40KB limit).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from pinecone import Pinecone
from tqdm import tqdm

load_dotenv()

RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

BATCH_SIZE = 100
TEXT_LIMIT = 1000  # metadata text truncation


def ingest(progress_callback=None):
    """Batch upsert embeddings into Pinecone vector index.

    Args:
        progress_callback: Optional callback(current, total) for progress updates.

    Returns:
        int: Number of vectors upserted.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Load texts from RAW_DIR / "corpus.jsonl" for metadata
        - Connect: Pinecone(api_key=...) → pc.Index(index_name)
        - Upsert format: {"id": ..., "values": [...], "metadata": {"text": ...}}
        - Batch size: BATCH_SIZE (100), truncate text to TEXT_LIMIT (1000) chars
    """
    # TODO: Implement Pinecone upsert
    embeddings = np.load(PROCESSED_DIR / "embeddings.npy")
    with open(PROCESSED_DIR / "embedding_ids.json", encoding="utf-8") as f:
        ids = json.load(f)

    id_to_text = {}
    with open(RAW_DIR / "corpus.jsonl", encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            id_to_text[str(doc["id"])] = doc["text"]

    api_key = os.getenv("PINECONE_API_KEY")
    index_name = os.getenv("PINECONE_INDEX")
    if not api_key or not index_name:
        raise ValueError("PINECONE_API_KEY / PINECONE_INDEX not set.")
    
    pinecone = Pinecone(api_key=api_key)
    index = pinecone.Index(index_name)

    total = len(ids)
    current = 0

    for start in range(0, total, BATCH_SIZE):
        end = start + BATCH_SIZE

        vectors = []
        for i in range(start, end):
            if i >= total:
                break

            doc_id = str(ids[i])
            text = id_to_text.get(doc_id, "")[:TEXT_LIMIT]

            vectors.append({
                "id": doc_id,
                "values": embeddings[i].tolist(),
                "metadata": {"text": text},
            })

        index.upsert(vectors=vectors)

        current = min(end, total)
        if progress_callback:
            progress_callback(current, total)

    return total


if __name__ == "__main__":
    ingest()
