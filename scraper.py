import yfinance as yf
import json
import time
import requests
import re

def get_all_leveraged_tickers():
    """스크리너를 통해 현재 시장의 모든 레버리지 ETF 티커를 먼저 가져옵니다."""
    print("🌐 실시간 레버리지 ETF 목록 탐색 중...")
    headers = {'User-Agent': 'Mozilla/5.0'}
    # 레버리지 ETF들만 모아놓은 스크리너 페이지 (예시: StockAnalysis 또는 유사 사이트)
    # 직접적인 API가 없으므로, 안정적인 쿼리 방식을 사용합니다.
    url = "https://api.stockanalysis.com/wp-json/sa/get_stock_list?type=etf&asset_class=Leveraged"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        data = response.json()
        # API에서 제공하는 전체 리스트에서 티커만 추출
        tickers = [item['s'] for item in data['data']]
        print(f"🔎 시장에서 {len(tickers)}개의 레버리지 종목을 발견했습니다.")
        return tickers
    except Exception as e:
        print(f"⚠️ 자동 탐색 실패, 비상용 리스트로 전환합니다: {e}")
        # 실패 시에만 보험용으로 주요 티커 사용
        return ["TQQQ", "SQQQ", "SOXL", "SOXS", "TSLL", "NVDL", "SPXL", "UPRO"]

def update_etf_rankings():
    # 1. 로봇이 스스로 명단 작성
    all_tickers = get_all_leveraged_tickers()
    
    final_data = []
    
    # 2. 각 티커별 상세 정보(AUM) 수집
    for ticker in all_tickers:
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 정확도 확보
            aum = info.get('totalAssets') or info.get('marketCap')
            
            if aum and aum >= 10_000_000: # $10MM 이상 필터링
                final_data.append({
                    "ticker": ticker,
                    "display_name": info.get('longName', ticker),
                    "aum": round(aum / 1_000_000, 2)
                })
                print(f"✅ 수집: {ticker}")
            
            time.sleep(0.1) # 밴 방지
        except:
            continue

    # 3. 정렬 및 저장
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    
    print(f"✨ 업데이트 완료: 총 {len(final_data)}개 종목")

if __name__ == "__main__":
    update_etf_rankings()
