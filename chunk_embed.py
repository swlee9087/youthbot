# chunk_embed.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from config import EMBED_MODEL

# 사전 로드
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
embedder = SentenceTransformer(EMBED_MODEL)

def chunk_and_embed(texts: list[str]) -> tuple[list[str], list[list[float]]]:
    all_chunks = []
    for text in texts:
        chunks = splitter.split_text(text)
        all_chunks.extend(chunks)

    embeddings = embedder.encode(all_chunks, show_progress_bar=False)
    return all_chunks, embeddings

def embed_query(query: str) -> list[float]:
    return embedder.encode([query])[0]
