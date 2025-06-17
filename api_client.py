# api_client.py

import requests
from config import API_KEYS, API_ENDPOINTS

def call_api(target: str, params: dict) -> list[str]:
    api_url = API_ENDPOINTS[target]
    api_key = API_KEYS[target]
    params["apiKeyNm"] = api_key

    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        json_data = response.json()
        return extract_text_list(json_data, target)

    except Exception as e:
        print(f"API 호출 실패: {e}")
        return []

def extract_text_list(json_data: dict, target: str) -> list[str]:
    items = json_data.get("result", {}).get("youthPolicyList", [])

    results = []
    for item in items:
        if target == "청년정책":
            text = "\n".join([
                f"정책명: {item.get('plcyNm', '')}",
                f"개요: {item.get('plcyExplnCn', '')}",
                f"지원내용: {item.get('plcySprtCn', '')}",
                f"신청방법: {item.get('plcyAplyMthdCn', '')}",
                f"신청URL: {item.get('aplyUrlAddr', '')}",
            ])
        elif target == "청년센터":
            text = "\n".join([
                f"센터명: {item.get('cntrNm', '')}",
                f"운영기관: {item.get('operInstNm', '')}",
                f"주소: {item.get('cntrAddr', '')} {item.get('cntrDaddr', '')}",
                f"운영시간: {item.get('cntrOperHrCn', '')}",
                f"전화번호: {item.get('cntrTelno', '')}",
            ])
        else:
            text = "지원 정책 정보가 없습니다."

        results.append(text)

    return results
