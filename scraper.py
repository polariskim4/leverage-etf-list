import yfinance as yf
import json
import time

def scrap_refined_leverage_dashboard():
    # 1. ETFdb 1~7페이지 기반 검증된 레버리지/인버스 티커 마스터 리스트
    # 일반 주식이나 현물 ETF와 겹치지 않는 티커들입니다.
    verified_list = [
        "TQQQ", "SQQQ", "QLD", "QID", "UPRO", "SPXU", "SSO", "SDS", "SPXL", "SPXS",
        "TECL", "TECS", "SOXL", "SOXS", "FAS", "FAZ", "TMF", "TMV", "LABU", "LABD",
        "YINN", "YANG", "NUGT", "DUST", "JNUG", "JDST", "FNGU", "FNGD", "BULZ", "BERZ",
        "TSLL", "TSLS", "NVDL", "NVDS", "AMZU", "AMZD", "MSFU", "MSFD", "AAPU", "AAPD",
        "CONL", "CONV", "BITX", "SBIT", "ETHU", "ETHS", "GGLL", "TNA", "TZA", "URTY",
        "SRTY", "TYD", "TYO", "UST", "PST", "UBT", "TBT", "UCO", "SCO", "BOIL", "KOLD",
        "AGQ", "ZSL", "UGL", "GLL", "GUSH", "DRIP", "ERX", "ERY", "DIG", "DUG",
        "KORU", "INDL", "MEXX", "EURL", "EDC", "EDZ", "DPST", "NAIL", "UVXY", "SVXY"
    ]

    # 2. 신규 상장 대비 자동 조합 (단, 이름 검증을 더 엄격하게 진행)
    bases = ["QQQ", "SPY", "SOX", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "META", "COIN", "BTC", "ETH"]
    prefixes = ["T", "S", "U", "D", "L", "F"]
    discovery_pool = list(set(verified_list + [p + b for p in prefixes for b in bases] + [b + "L" for b in bases] + [b + "S" for b in bases]))

    final_results = []
    print(f"📡 총 {len(discovery_pool)}개 종목 정밀 검사 중... (가짜 종목 차단 모드)")

    for ticker in discovery_pool:
        # GOOGL, FBTC, ERO 등 제외 대상 필터링
        if ticker in ["GOOGL", "GOOG", "FBTC", "ERO", "FETH", "AAPL", "MSFT", "TSLA", "NVDA"]:
            continue

        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 필터 ($10MM 이상)
            aum = info.get('totalAssets') or info.get('marketCap')
            if not aum or aum < 10_000_000:
                continue

            name = info.get('longName', '')
            # 핵심 필터: 이름에 반드시 아래 레버리지 관련 키워드가 있어야 함
            # 'Alphabet Inc.' 같은 일반 주식은 여기서 탈락함
            lev_keywords = ['Leveraged', 'Bull', 'Bear', '2x', '3x', 'Short', 'Ultra', 'Inverse', 'Daily', 'Strategy']
            
            is_leveraged = any(k.lower() in name.lower() for k in lev_keywords)
            
            # 검증된 리스트에 있거나, 이름에 레버리지 키워드가 포함된 경우만 최종 승인
            if is_leveraged or ticker in verified_list:
                final_results.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2)
                })
                print(f"✅ 승인: {ticker} - {name}")
            
            time.sleep(0.05)
        except:
            continue

    # AUM 순 정렬
    final_results = sorted(final_results, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    print(f"✨ 정제 완료! 총 {len(final_results)}개의 순수 레버리지 종목이 저장되었습니다.")

if __name__ == "__main__":
    scrap_refined_leverage_dashboard()
