# main.py
from pdf_loader import load_pdfs_from_local_repo
import time
import streamlit as st
from parser import parse_input
from api_client import call_api
from chunk_embed import chunk_and_embed, embed_query
from vector_store import search_top_k
from llm_generator import generate_answer
from logger import logger

if "history" not in st.session_state:
    st.session_state.history = []
if "answer" not in st.session_state: # 답변을 저장할 세션 상태 추가
    st.session_state.answer = None
if "user_input_key" not in st.session_state: # 입력창 초기화를 위한 key 추가
    st.session_state.user_input_key = 0

    
st.set_page_config(page_title="청년정책 RAG 챗봇", layout="centered")
st.title("🧠 청년정책 정보 RAG 챗봇")

# setup.py 혹은 main.py 상단
@st.cache_resource
def load_pdf_embeddings():
    docs = load_pdfs_from_local_repo()  # GitHub 클론된 경로 기준
    chunks, embeddings = chunk_and_embed(docs)
    return chunks, embeddings

pdf_chunks, pdf_embs = load_pdf_embeddings()

def process_query():
    user_query = st.session_state.user_input
    if not user_query:
        return
    start_time = time.time()
    current_answer = None # 현재 처리 중인 답변을 저장할 변수
    user_query = st.text_input(
        "📌 질문을 입력하세요:",
        placeholder="예: 김천의 청년센터 위치는?",
        key="user_input"
    )

    if user_query:
        with st.spinner("처리 중입니다..."):
            try:
                parsed = parse_input(user_query)
                docs = call_api(parsed["target"], parsed["params"])

                if not docs:
                    # st.error("❌ 관련 정보를 찾을 수 없습니다.")
                    elapsed = round(time.time() - start_time, 2)
                    answer = f"❌ 관련 정보를 찾을 수 없습니다.\n\n⏱️ 처리 시간: {elapsed}초"
                    logger.warning("API 응답 문서 없음.")
                else:
                    chunks, doc_embs = chunk_and_embed(docs)
                    if not chunks or not doc_embs:
                        # answer = "📭 관련된 문서를 찾을 수 없었습니다."
                        elapsed = round(time.time() - start_time, 2)
                        current_answer  = f"📭 관련된 문서를 찾을 수 없었습니다.\n\n⏱️ 처리 시간: {elapsed}초"
                        st.warning("📭 관련된 문서를 찾을 수 없었습니다.")
                        logger.warning("임베딩 후 문서 없음.")
                    else:
                        query_emb = embed_query(user_query)
                        top_k_idx = search_top_k(query_emb, doc_embs, k=3)
                        top_docs = [chunks[i] for i in top_k_idx]
                        if not top_docs:
                            # st.warning("🔍 유사한 문서를 찾지 못했습니다.")
                            elapsed = round(time.time() - start_time, 2)
                            current_answer  = f"🔍 유사한 문서를 찾지 못했습니다.\n\n⏱️ 처리 시간: {elapsed}초"
                            logger.warning("Top-K 유사 문서 없음.")
                        else: 
                            # answer = generate_answer(user_query, top_docs)
                            raw_answer = generate_answer(user_query, top_docs)
                            elapsed = round(time.time() - start_time, 2)
                            current_answer  = f"{raw_answer}\n\n⏱️ 처리 시간: {elapsed}초"
                    # st.subheader("✅ 답변")
                    # st.markdown(answer)
                    
                    # 💾 히스토리에 저장
                st.session_state.history.append((user_query, answer))
                st.session_state.user_input = ""  # 입력창 초기화
                st.session_state.user_input_key += 1 # 입력창 key를 변경하여 재생성 (초기화 효과)
                
            except Exception as e:
                elapsed = round(time.time() - start_time, 2)
                current_answer  = f"❌ 처리 중 오류 발생\n\n⏱️ 처리 시간: {elapsed}초"
                logger.exception(f"Streamlit 처리 중 예외 발생: {e}")
                # # st.error("앱 실행 중 오류 발생 ❌")
                st.session_state.history.append((user_query, "❌ 처리 중 오류 발생"))
                st.session_state.user_input = ""
                st.session_state.user_input_key += 1
                
# 입력창을 폼으로 감싸서 제출 버튼 클릭 시에만 process_query 함수가 실행되도록 합니다.
# 또한, key를 변경하여 입력창을 초기화하는 트릭을 사용합니다.
with st.form(key=f"query_form_{st.session_state.user_input_key}"):
    user_query_input = st.text_input(
        "📌 질문을 입력하세요:",
        placeholder="예: 김천의 청년센터 위치는?",
        key="user_input", # 이 key는 process_query 함수에서 st.session_state.user_input으로 접근
        label_visibility="collapsed" # 레이블을 숨겨서 깔끔하게
    )
    submit_button = st.form_submit_button("질문하기")

    if submit_button:
        process_query() # 제출 버튼 클릭 시에만 쿼리 처리 함수 호출

# 📜 누적된 대화 출력
for q, a in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(f"**질문:** {q}")
    with st.chat_message("assistant"):
        st.markdown(f"**답변:** {a}")