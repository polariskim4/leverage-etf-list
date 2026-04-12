import yfinance as yf
import json
import time

def scrap_final_leverage_dashboard():
    # 1. ETFdb의 모든 페이지를 아우르는 방대한 누락 방지 리스트 (200개+)
    # 지수, 섹터, 원자재, 채권, 통화 등 모든 레버리지/인버스 포함
    core_list = [
        # --- 대표 지수 (나스닥, S&P500, 다우, 러셀) ---
        "TQQQ", "SQQQ", "QLD", "QID", "UPRO", "SPXU", "SSO", "SDS", "SPXL", "SPXS",
        "UDOW", "SDOW", "DDM", "DXD", "TNA", "TZA", "UWM", "TWM", "URTY", "SRTY",
        "MIDU", "TYD", "TYO", "UMDD", "SMDD", "UVXY", "SVXY", "VIXY",

        # --- 빅테크 및 반도체 ---
        "SOXL", "SOXS", "USD", "SSG", "TECL", "TECS", "FNGU", "FNGD", "BULZ", "BERZ",
        "NVDL", "NVDS", "TSLL", "TSLS", "AMZU", "AMZD", "MSFU", "MSFD", "AAPU", "AAPD",
        "GOOGL", "GOOGS", "FBLL", "FBLS", "CONL", "CONV",

        # --- 섹터별 (금융, 에너지, 바이오, 부동산 등) ---
        "FAS", "FAZ", "ERX", "ERY", "DIG", "DUG", "GUSH", "DRIP", "LABU", "LABD",
        "CURE", "SICK", "DRN", "DRV", "NAIL", "RAIL", "RETL", "DPST", "WANT", "TPOR",
        "UTSL", "PILL", "HIBL", "HIBS", "PILL", "OOTO",

        # --- 채권, 금리, 통화 ---
        "TMF", "TMV", "TYD", "TYO", "UST", "PST", "UBT", "TBT", "TTT", "TBX",
        "YCS", "YCL", "UUP", "UDN", "EUO", "ERO",

        # --- 원자재 (금, 은, 오일, 천연가스) ---
        "UCO", "SCO", "BOIL", "KOLD", "UNG", "UGL", "GLL", "AGQ", "ZSL", "NUGT", "DUST",
        "JNUG", "JDST", "USL", "DGP", "DZZ",

        # --- 글로벌 및 신흥국 ---
        "YINN", "YANG", "EDC", "EDZ", "MEXX", "EURL", "KORU", "INDL", "LBJ", "EUM", "EEV",

        # --- 암호화폐 및 기타 신규 ---
        "BITO", "BITX", "SBIT", "ETHU", "ETHS", "GGLL", "TSL"
    ]

    # 2. 신규 종목 대비용 자동 조합 로직 (Prefix + Base)
    bases = ["QQQ", "SPY", "SOX", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "META", "COIN", "ETH", "BTC"]
    prefixes = ["T", "S", "U", "D", "L", "F"]
    generated = []
    for b in bases:
        for p in prefixes:
            generated.append(p + b)
            generated.append(b + "L")
            generated.append(b + "S")

    # 3. 중복 제거 및 최종 탐색 풀 구성
    search_pool = list(set(core_list + generated))
    
    final_results = []
    print(f"📡 총 {len(search_pool)}개 종목 전수 조사 시작... (조건: AUM $10MM 이상)")

    for ticker in search_pool:
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 정확도 최우선: totalAssets -> marketCap 순서
            aum = info.get('totalAssets') or info.get('marketCap')
            
            # $10MM 이상 필터링
            if aum and aum >= 10_000_000:
                name = info.get('longName', ticker)
                final_results.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2) # Million 달러
                })
                print(f"✅ 수집: {ticker} (${round(aum/1_000_000)}MM)")
            
            time.sleep(0.05) # 빠른 수집을 위해 지연시간 단축
        except:
            continue

    # 4. AUM 순으로 정렬
    final_results = sorted(final_results, key=lambda x: x['aum'], reverse=True)

    # 5. 데이터 저장
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_results, f, ensure_ascii=False, indent=4)
    
    print(f"🎉 갱신 완료! 총 {len(final_results)}개의 종목이 리스트에 올라왔습니다.")

if __name__ == "__main__":
    scrap_final_leverage_dashboard()
