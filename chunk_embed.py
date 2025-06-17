# chunk_embed.py

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from sentence_transformers import SentenceTransformer
# from config import EMBED_MODEL

# # 사전 로드
# splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)
# embedder = SentenceTransformer(EMBED_MODEL)

# def chunk_and_embed(texts: list[str]) -> tuple[list[str], list[list[float]]]:
#     all_chunks = []
#     for text in texts:
#         chunks = splitter.split_text(text)
#         all_chunks.extend(chunks)

#     embeddings = embedder.encode(all_chunks, show_progress_bar=False)
#     return all_chunks, embeddings

# def embed_query(query: str) -> list[float]:
#     return embedder.encode([query])[0]


from langchain.text_splitter import RecursiveCharacterTextSplitter
from config import OPENAI_API_KEY, EMBED_MODEL
import openai

openai.api_key = OPENAI_API_KEY
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)

def chunk_and_embed(texts: list[str]) -> tuple[list[str], list[list[float]]]:
    all_chunks = []
    for text in texts:
        all_chunks.extend(splitter.split_text(text))

    embeddings = []
    for chunk in all_chunks:
        res = openai.embeddings.create(model=EMBED_MODEL, input=chunk)
        embeddings.append(res.data[0].embedding)

    return all_chunks, embeddings

def embed_query(query: str) -> list[float]:
    res = openai.embeddings.create(model=EMBED_MODEL, input=query)
    return res.data[0].embedding
