import yfinance as yf
import json
import time

def scrap_perfect_leverage_list():
    # 1. 누락되었던 종목들을 포함한 '확장된 마스터 리스트'
    # 조합으로 안 나오는 종목들(AGQ, SCO, KORU 등)을 대거 포함
    master_candidates = [
        "FAS", "FAZ", "AGQ", "ZSL", "FNGU", "FNGD", "TNA", "TZA", "KORU", "NUGT", "DUST",
        "SCO", "UCO", "UGL", "GLL", "ETHU", "ETHS", "BITO", "BITX", "CONL", "NVDL", "TSLL",
        "TQQQ", "SQQQ", "SOXL", "SOXS", "SPXL", "SPXS", "UPRO", "SPXU", "LABU", "LABD",
        "YINN", "YANG", "EURL", "MEXX", "EDC", "EDZ", "INDL", "CURE", "WANT", "DPST"
    ]
    
    # 2. 기존의 조합 로직도 병행 (신규 종목 대비)
    bases = ["QQQ", "SPY", "SOX", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "META", "COIN", "ETH", "BTC"]
    prefixes = ["T", "S", "U", "D", "L", "F"]
    for b in bases:
        for p in prefixes:
            master_candidates.append(p + b)
            master_candidates.append(b + p)
            master_candidates.append(b + "L")
            master_candidates.append(b + "S")

    unique_candidates = list(set(master_candidates))
    final_data = []
    
    print(f"📡 총 {len(unique_candidates)}개 종목 정밀 필터링 시작...")

    for ticker in unique_candidates:
        try:
            etf = yf.Ticker(ticker)
            # AUM 정확도를 위해 totalAssets를 1순위로 호출
            info = etf.info
            aum = info.get('totalAssets') or info.get('marketCap')
            
            # $10MM 이상 필터링
            if aum and aum >= 10_000_000:
                name = info.get('longName', '')
                # 레버리지/인버스 키워드 검증
                keywords = ['Leveraged', 'Bull', 'Bear', '2x', '3x', 'Short', 'Ultra', 'Inverse']
                
                if any(k in name for k in keywords) or ticker in ["TQQQ", "SOXL", "NVDL", "TSLL"]:
                    final_data.append({
                        "ticker": ticker,
                        "display_name": name,
                        "aum": round(aum / 1_000_000, 2)
                    })
                    print(f"✅ 발견: {ticker} (${round(aum/1_000_000)}MM)")
            
            time.sleep(0.05)
        except:
            continue

    # AUM 순 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"🎉 갱신 완료! 총 {len(final_data)}개 종목이 표시됩니다.")

if __name__ == "__main__":
    scrap_perfect_leverage_list()
