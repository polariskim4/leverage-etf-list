import yfinance as yf
import json
import time

def get_leveraged_etf_rankings():
    # 시장에서 유명한 레버리지 ETF들을 최대한 많이 리스트업합니다.
    # 로봇은 여기서 진짜 자산 규모(AUM)가 큰 것들을 골라냅니다.
    tickers = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "UPRO", "SPXU", "FNGU", "FNGD", 
        "TNA", "TZA", "BULZ", "BERZ", "LABU", "LABD", "YINN", "YANG",
        "TECL", "TECS", "UVXY", "SVXY", "BITO", "USD", "SSG", "DRN", "DRV",
        "QLD", "QID", "SSO", "SDS", "UWM", "TWM", "DIG", "DUG", "UYG", "SKF"
    ]
    
    final_data = []
    print(f"🚀 총 {len(tickers)}개 후보 종목 탐색 시작...")

    for ticker in tickers:
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM (Total Assets) 정보 가져오기
            aum = info.get('totalAssets')
            name = info.get('longName', f"{ticker} Leverage ETF")
            
            if aum:
                # 단위를 Million($MM, 백만 달러)으로 변환
                aum_mm = round(aum / 1_000_000, 2)
                final_data.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": aum_mm
                })
                print(f"✅ {ticker}: ${aum_mm}MM 확인")
            
            time.sleep(0.2) # 차단 방지용 휴식
        except Exception as e:
            print(f"❌ {ticker} 수집 실패")
            continue

    # AUM(자산 규모)이 큰 순서대로 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    # 데이터가 정상적으로 수집되었을 때만 저장
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"🎉 총 {len(final_data)}개 종목 순위 업데이트 완료!")
    else:
        print("🚨 수집된 데이터가 없습니다.")

if __name__ == "__main__":
    get_leveraged_etf_rankings()
