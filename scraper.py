import yfinance as yf
import json
import time

def get_etf_data():
    tickers = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "UPRO", "SPXU", "FNGU", "FNGD", 
        "TNA", "TZA", "BULZ", "BERZ", "LABU", "LABD", "YINN", "YANG",
        "TECL", "TECS", "BITO", "USD", "QLD", "QID", "SSO", "SDS",
        "FAS", "FAZ", "ERX", "ERY", "GUSH", "DRIP", "DFEN", "NUGT", "DUST"
    ]
    
    results = []
    print(f"🚀 총 {len(tickers)}개 종목 수집 시작...")

    for ticker in tickers:
        try:
            etf = yf.Ticker(ticker)
            # 가장 안전한 기본 info 사용
            data = etf.info
            
            # 자산 규모(AUM) 또는 시가총액 가져오기
            aum = data.get('totalAssets') or data.get('marketCap') or data.get('navPrice', 0)
            name = data.get('longName', ticker)
            
            # 데이터가 있으면 일단 저장
            results.append({
                "ticker": ticker,
                "display_name": name,
                "aum": round(aum / 1_000_000, 2) if aum else 0
            })
            print(f"✅ {ticker} 수집 성공")
            
            time.sleep(0.5) 
        except Exception as e:
            print(f"❌ {ticker} 실패: {e}")
            continue

    # AUM 순서로 정렬 (데이터가 없는 건 뒤로)
    results = sorted(results, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"🎉 총 {len(results)}개 종목 업데이트 완료!")

if __name__ == "__main__":
    get_etf_data()
