import yfinance as yf
import json
import time

def get_leveraged_etf_rankings():
    # 수집할 대표적인 레버리지 ETF 리스트
    tickers = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "UPRO", "SPXU", "FNGU", "FNGD", 
        "TNA", "TZA", "BULZ", "BERZ", "LABU", "LABD", "YINN", "YANG",
        "TECL", "TECS", "BITO", "USD", "QLD", "QID", "SSO", "SDS"
    ]
    
    final_data = []
    print(f"🔎 {len(tickers)}개 종목 수집 시작...")

    for ticker in tickers:
        try:
            etf = yf.Ticker(ticker)
            info = etf.fast_info # 더 빠른 데이터 수집 방식 사용
            
            # 자산 규모(AUM) 가져오기
            aum = info.get('market_cap', 0) # market_cap으로 대체하여 더 정확하게 수집
            
            # 종목 전체 이름 가져오기
            full_name = etf.info.get('longName', f"{ticker} Leverage ETF")
            
            if aum > 0:
                final_data.append({
                    "ticker": ticker,
                    "display_name": full_name,
                    "aum": round(aum / 1_000_000, 2) # Million($) 단위로 변환
                })
                print(f"✅ {ticker} 수집 완료")
            else:
                print(f"⚠️ {ticker} 데이터 없음 (AUM 0)")
            
            time.sleep(0.1) # 서버 차단 방지
        except Exception as e:
            print(f"❌ {ticker} 오류 발생: {e}")
            continue

    # AUM(자산 규모)이 큰 순서대로 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    # 데이터 저장
    if final_data:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(final_data, f, ensure_ascii=False, indent=4)
        print(f"🎉 총 {len(final_data)}개 종목 업데이트 성공!")
    else:
        print("🚨 수집된 데이터가 하나도 없습니다. 코드를 다시 점검해야 합니다.")

if __name__ == "__main__":
    get_leveraged_etf_rankings()
