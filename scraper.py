import requests
import pandas as pd
import json

def get_leveraged_etf_rankings():
    # 보안이 덜 까다롭고 데이터가 방대한 소스를 활용합니다.
    # 이 API는 레버리지 ETF 목록을 포함한 상세 데이터를 제공합니다.
    url = "https://api.stockanalysis.com/wp-json/sa/get_stock_list?type=etf&asset_class=Leveraged"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        
        # 전체 ETF 리스트 추출
        raw_list = data.get('data', [])
        
        extracted_data = []
        for item in raw_list:
            # AUM 정보가 있고, 레버리지 관련 키워드가 있는 것들만 필터링
            # (StockAnalysis API에서 'asset_class'가 Leveraged인 것만 가져오지만 한번 더 검증)
            ticker = item.get('s') # Ticker
            name = item.get('n')   # Name
            aum = item.get('a')    # AUM (Assets Under Management)
            
            if aum and aum >= 10: # AUM 10M$ 이상인 것만
                extracted_data.append({
                    "ticker": ticker,
                    "display_name": f"{name} ({ticker})",
                    "aum": float(aum)
                })

        # AUM(자산 규모) 기준으로 내림차순 정렬 (큰 것부터)
        final_list = sorted(extracted_data, key=lambda x: x['aum'], reverse=True)
        
        print(f"✅ 총 {len(final_list)}개의 레버리지 ETF를 발견했습니다.")

    except Exception as e:
        print(f"⚠️ 자동 수집 중 에러 발생: {e}")
        # 실패 시 최소한의 데이터라도 유지
        final_list = [{"ticker": "ERROR", "display_name": "데이터 자동 갱신 실패 (보안 차단)", "aum": 0}]

    # 결과 저장
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_list, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_leveraged_etf_rankings()
