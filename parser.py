# parser.py

def parse_input(user_query: str) -> dict:
    query = user_query.strip()

    # 우선순위: 센터 > 정책 > 법률
    if any(word in query for word in ["센터", "위치", "주소"]):
        return {
            "target": "청년센터",
            "params": {
                "pageNum": 1,
                "pageSize": 1000,
                "rtnType": "json",
                "ctpvCd": "",  # 시/도 코드 추출 가능 시 삽입
                "sggCd": "",   # 시/군/구 코드 추출 가능 시 삽입
            }
        }

    elif any(word in query for word in ["정책", "대출", "지원", "청년"]):
        return {
            "target": "청년정책",
            "params": {
                "pageNum": 1,
                "pageSize": 1000,
                "rtnType": "json",
                "plcyKywdNm": "",  # 키워드 분석 결과 삽입 가능
                "zipCd": "",       # 지역 우편번호 추출 시 삽입
            }
        }

    else:
        return {
            "target": "청년정책",
            "params": {
                "pageNum": 1,
                "pageSize": 1000,
                "rtnType": "json",
            }
        }
