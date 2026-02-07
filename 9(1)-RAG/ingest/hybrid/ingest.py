"""Ingest corpus into Elasticsearch Hybrid index (wiki-hybrid).

Index mapping: text field + dense_vector(4096, cosine).
Bulk chunk_size=100 (heavier with 4096-dim vectors).
"""

import json
import os
from pathlib import Path

import numpy as np
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from tqdm import tqdm

load_dotenv()

INDEX_NAME = "wiki-hybrid"
RAW_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "raw"
PROCESSED_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "processed"

INDEX_MAPPINGS = {
    "properties": {
        "text": {"type": "text", "analyzer": "standard"},
        "embedding": {
            "type": "dense_vector",
            "dims": 4096,
            "index": True,
            "similarity": "cosine",
        },
    }
}


def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        os.getenv("ELASTIC_ENDPOINT"),
        api_key=os.getenv("ELASTIC_API_KEY"),
        request_timeout=120,
    )


def _generate_actions(corpus_path: Path, embeddings: np.ndarray, ids: list[str]):
    id_to_idx = {doc_id: idx for idx, doc_id in enumerate(ids)}

    with open(corpus_path, encoding="utf-8") as f:
        for line in f:
            doc = json.loads(line)
            doc_id = doc["id"]
            idx = id_to_idx.get(doc_id)
            if idx is None:
                continue
            yield {
                "_index": INDEX_NAME,
                "_id": doc_id,
                "_source": {
                    "text": doc["text"],
                    "embedding": embeddings[idx].tolist(),
                },
            }


def ingest(progress_callback=None):
    """Create hybrid index (text + dense_vector) and bulk-ingest corpus.

    Args:
        progress_callback: Optional callback(count) called after completion.

    Returns:
        int: Number of documents indexed.

    Hints:
        - Load embeddings from PROCESSED_DIR / "embeddings.npy"
        - Load IDs from PROCESSED_DIR / "embedding_ids.json"
        - Use get_es_client(), delete/create index with INDEX_MAPPINGS
        - Use _generate_actions(corpus_path, embeddings, ids) for bulk data
        - Use elasticsearch.helpers.bulk() with chunk_size=100
        - Call es.indices.refresh() after bulk ingest
    """
    # TODO: Implement ES Hybrid ingestion
    emb_path = PROCESSED_DIR / "embeddings.npy"
    ids_path = PROCESSED_DIR / "embedding_ids.json"

    embeddings = np.load(emb_path)
    with open(ids_path, encoding="utf-8") as f:
        ids = json.load(f)
    
    es = get_es_client()

    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
    
    es.indices.create(index=INDEX_NAME, mappings=INDEX_MAPPINGS)

    corpus_path = RAW_DIR / "corpus.jsonl"
    
    total_lines = 0
    with open(corpus_path, encoding="utf-8") as f:
        for i in f:
            total_lines += 1

    indexed_count = 0
    actions = _generate_actions(corpus_path, embeddings, ids)

    with tqdm(total=total_lines, desc="Ingesting Hybrid corpus", unit="doc") as pbar:
        def actions_with_progress():
            nonlocal indexed_count
            for act in actions:
                yield act
                indexed_count += 1
                pbar.update(1)

        bulk(es, actions_with_progress(), chunk_size=100)
    
    es.indices.refresh(index=INDEX_NAME)

    if progress_callback:
        progress_callback(indexed_count)

    return indexed_count


if __name__ == "__main__":
    ingest()
