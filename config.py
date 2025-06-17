# config.py

import os
from dotenv import load_dotenv

load_dotenv()  # .env 파일 불러오기

API_KEYS = {
    "청년정책": os.getenv("YOUTH_POLICY_API_KEY"),
    "청년센터": os.getenv("YOUTH_CENTER_API_KEY"),
}

API_ENDPOINTS = {
    "청년정책": "https://www.youthcenter.go.kr/go/ythip/getPlcy",
    "청년센터": "https://www.youthcenter.go.kr/go/ythip/getSpace",
}

# 임베딩 모델 이름
EMBED_MODEL = "jhgan/ko-sroberta-multitask"

# LLM 모델 이름
LLM_MODEL = "google/gemma-3-1b-it"


# config.py

import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-3.5-turbo"
