# vector_store.py

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def search_top_k(query_emb: list[float], doc_embs: list[list[float]], k: int = 3) -> list[int]:
    sims = cosine_similarity([query_emb], doc_embs)[0]
    top_k_idx = np.argsort(sims)[-k:][::-1]
    return top_k_idx.tolist()
