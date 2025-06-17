# config.py

# API Key 설정
API_KEYS = {
    "청년정책": "4efec90c-a726-45ea-859e-4b4c52c6955f",
    "청년센터": "c55365a2-5fa9-48c2-bd3f-f63bf0ee3b61",
}

# API 엔드포인트
API_ENDPOINTS = {
    "청년정책": "https://www.youthcenter.go.kr/go/ythip/getPlcy",
    "청년센터": "https://www.youthcenter.go.kr/go/ythip/getSpace",
}

# 임베딩 모델 이름
EMBED_MODEL = "jhgan/ko-sroberta-multitask"

# LLM 모델 이름
LLM_MODEL = "google/gemma-3-1b-it"
