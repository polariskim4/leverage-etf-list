import yfinance as yf
import json
import time

def get_dynamic_leverage_list():
    # 1. 주요 레버리지 운용사들이 사용하는 '핵심 티커'와 '레버리지 접미사' 조합
    # 로봇이 이들을 조합하여 수백 개의 가능성을 스스로 검사합니다.
    bases = ["QQQ", "SOX", "SPY", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "FNG", "LAB", "FINL", "EMG", "KOR", "CHN"]
    prefixes = ["T", "S", "U", "D", "L", "F"] # TQQQ, SQQQ, UPRO 등
    suffixes = ["L", "S", "X", "U", "D"]    # SOXL, SOXS 등
    
    # 2. 알려진 모든 레버리지 티커를 일단 다 때려넣습니다 (여기에 신규 종목 계속 추가 가능)
    # 이 리스트는 계속 확장되어도 상관없습니다. 로봇이 걸러줄 테니까요.
    discovery_pool = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "SPXL", "SPXS", "UPRO", "SPXU", "TSLL", "TSLS", "NVDL", "NVDS",
        "FNGU", "FNGD", "BULZ", "BERZ", "TECL", "TECS", "LABU", "LABD", "YINN", "YANG", "TMF", "TMV",
        "BITO", "BITX", "FAS", "FAZ", "UCO", "SCO", "BOIL", "KOLD", "GUSH", "DRIP", "DPST", "NAIL"
    ]
    
    # 조합 생성 (예: NVDA + L = NVDL)
    for b in bases:
        for p in prefixes: discovery_pool.append(p + b)
        for s in suffixes: discovery_pool.append(b + s)

    # 중복 제거
    discovery_pool = list(set(discovery_pool))
    
    final_data = []
    print(f"📡 총 {len(discovery_pool)}개 가능성 탐색 중... ($10MM 이상 자동 선별)")

    for ticker in discovery_pool:
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 데이터 정확도: totalAssets -> marketCap 순서
            aum = info.get('totalAssets') or info.get('marketCap')
            
            # $10,000,000 이상인 것만 저장
            if aum and aum >= 10_000_000:
                name = info.get('longName', ticker)
                final_data.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2)
                })
                print(f"✅ 발견: {ticker} (${round(aum/1_000_000, 1)}MM)")
            
            time.sleep(0.05) # 매우 빠른 탐색
        except:
            continue

    # AUM 순 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"🎉 총 {len(final_data)}개 종목 업데이트 완료!")

if __name__ == "__main__":
    get_dynamic_leverage_list()
