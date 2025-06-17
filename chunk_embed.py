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
from logger import logger

openai.api_key = OPENAI_API_KEY
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=100)

# def chunk_and_embed(texts: list[str]) -> tuple[list[str], list[list[float]]]:
#     all_chunks = []
#     for text in texts:
#         all_chunks.extend(splitter.split_text(text))

#     embeddings = []
#     for chunk in all_chunks:
#         res = openai.embeddings.create(model=EMBED_MODEL, input=chunk)
#         embeddings.append(res.data[0].embedding)

#     return all_chunks, embeddings
def chunk_and_embed(texts: list[str]) -> tuple[list[str], list[list[float]]]:
    all_chunks = []
    for text in texts:
        chunks = splitter.split_text(text)
        if not chunks:
            logger.warning(f"빈 텍스트에서 청크 생성 실패: {text[:50]}...")
        all_chunks.extend(chunks)

    embeddings = []
    for chunk in all_chunks:
        try:
            res = openai.embeddings.create(model=EMBED_MODEL, input=chunk)
            embeddings.append(res.data[0].embedding)
        except Exception as e:
            logger.exception(f"임베딩 실패: {chunk[:50]}... → {e}")
            continue

    return all_chunks, embeddings

def embed_query(query: str) -> list[float]:
    res = openai.embeddings.create(model=EMBED_MODEL, input=query)
    return res.data[0].embedding
