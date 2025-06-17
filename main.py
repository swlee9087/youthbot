# main.py

import streamlit as st
from parser import parse_input
from api_client import call_api
from chunk_embed import chunk_and_embed, embed_query
from vector_store import search_top_k
from llm_generator import generate_answer

st.set_page_config(page_title="청년정책 RAG 챗봇", layout="centered")
st.title("🧠 청년정책 정보 RAG 챗봇")

user_query = st.text_input("📌 질문을 입력하세요:")

# if user_query:
#     with st.spinner("처리 중입니다..."):
#         parsed = parse_input(user_query)
#         docs = call_api(parsed["target"], parsed["params"])

#         if not docs:
#             st.error("❌ 관련 정보를 찾을 수 없습니다.")
#         else:
#             chunks, doc_embs = chunk_and_embed(docs)
#             query_emb = embed_query(user_query)
#             top_k_idx = search_top_k(query_emb, doc_embs, k=3)
#             top_docs = [chunks[i] for i in top_k_idx]
#             answer = generate_answer(user_query, top_docs)

#             st.subheader("✅ 답변")
#             st.markdown(answer)


from logger import logger

if user_query:
    with st.spinner("처리 중입니다..."):
        try:
            parsed = parse_input(user_query)
            docs = call_api(parsed["target"], parsed["params"])

            if not docs:
                st.error("❌ 관련 정보를 찾을 수 없습니다.")
                logger.warning("API 응답 문서 없음.")
            else:
                chunks, doc_embs = chunk_and_embed(docs)
                query_emb = embed_query(user_query)
                top_k_idx = search_top_k(query_emb, doc_embs, k=3)
                top_docs = [chunks[i] for i in top_k_idx]
                answer = generate_answer(user_query, top_docs)
                st.subheader("✅ 답변")
                st.markdown(answer)

        except Exception as e:
            st.error("앱 실행 중 오류 발생 ❌")
            logger.exception(f"Streamlit 처리 중 예외 발생: {e}")
