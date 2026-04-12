import yfinance as yf
import json
import time

def get_etf_data():
    # 수집할 주요 레버리지 ETF들 (리스트를 대폭 늘렸습니다)
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
            # 자산 규모(AUM) 대용으로 시가총액 데이터를 사용합니다.
            info = etf.fast_info
            aum = info.get('market_cap', 0) 
            
            # 종목명 가져오기
            full_name = etf.info.get('longName', f"{ticker} Leverage ETF")
            
            if aum > 0:
                results.append({
                    "ticker": ticker,
                    "display_name": full_name,
                    "aum": round(aum / 1_000_000, 2) # Million($) 단위
                })
                print(f"✅ {ticker} 완료")
            
            time.sleep(0.2) # 과부하 방지
        except:
            continue

    # AUM이 큰 순서대로 정렬
    results = sorted(results, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"🎉 총 {len(results)}개 종목 업데이트 완료!")

if __name__ == "__main__":
    get_etf_data()
