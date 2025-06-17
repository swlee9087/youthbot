# llm_generator.py

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from config import LLM_MODEL

device = "cuda" if torch.cuda.is_available() else "cpu"
dtype = torch.float16 if device == "cuda" else torch.float32

print(f"LLM 로딩 중... ({device})")

# 모델 및 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    LLM_MODEL,
    torch_dtype=dtype,
    device_map="auto" if device == "cuda" else None
).to(device)

def generate_answer(question: str, top_docs: list[str]) -> str:
    context = "\n\n".join(top_docs)
    prompt = (
        f"다음은 청년 정책 또는 센터 관련 정보입니다:\n{context}\n\n"
        f"이 정보를 참고해, 아래 질문에 대해 간결하고 구체적으로 답변해 주세요.\n"
        f"질문: {question}\n"
        f"답변:"
    )

    # 토크나이즈
    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024).to(device)

    # 생성
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=256,
            num_beams=3,
            early_stopping=True,
            no_repeat_ngram_size=2
        )

    # 디코드
    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return decoded.split("답변:")[-1].strip()
