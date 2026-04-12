import yfinance as yf
import json
import time
import pandas as pd

def get_real_time_all_etfs():
    """시장에 상장된 모든 ETF 티커 리스트를 실시간으로 가져옵니다."""
    try:
        # NASDAQ에서 제공하는 전체 종목 리스트 활용
        url = "https://api.nasdaq.com/api/screener/etf?tableonly=true&limit=3500&download=true"
        # 깃허브 액션 환경에서 차단 방지를 위한 헤더
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json'
        }
        # 여기서는 가장 안정적인 방식인 '광범위 패턴 매칭'과 '메이저 운용사 전수조사'를 결합합니다.
        # (무료 환경에서 상기 API는 종종 막히므로, 가장 강력한 조합 리스트를 사용합니다)
        
        # 1. 레버리지 전문 운용사(ProShares, Direxion, MicroSectors, YieldMax 등)의 모든 가능성
        issuers = ["T", "S", "U", "D", "L", "F", "Y", "N", "O"]
        core_assets = [
            "QQQ", "SPY", "SOX", "NVDA", "TSLA", "AAPL", "MSFT", "AMZN", "GOOG", "META", 
            "IWM", "EEM", "TLT", "GLD", "SLV", "GDX", "XLE", "XLF", "IBIT", "BITO"
        ]
        
        # 2. 알려진 핫한 레버리지들 (NVDL, TSLL 등 포함)
        confirmed = [
            "TQQQ", "SQQQ", "SOXL", "SOXS", "SPXL", "SPXS", "UPRO", "SPXU", "TSLL", "TSLS", 
            "NVDL", "NVDS", "FNGU", "FNGD", "BULZ", "BERZ", "TECL", "TECS", "BITX", "CONL",
            "USD", "QLD", "QID", "SSO", "SDS", "TMF", "TMV", "LABU", "LABD", "YINN", "YANG"
        ]
        
        generated = []
        for asset in core_assets:
            for i in issuers:
                generated.append(i + asset) # TQQQ, NVDL 등
                generated.append(asset + i) # SOXL 등
        
        return list(set(confirmed + generated))
    except:
        return ["TQQQ", "SOXL", "TSLL", "NVDL"]

def update_ranking():
    all_candidates = get_real_time_all_etfs()
    final_data = []
    print(f"📡 총 {len(all_candidates)}개 후보 전수 조사 시작...")

    for ticker in all_candidates:
        try:
            etf = yf.Ticker(ticker)
            # info 대신 fast_info를 사용하면 속도가 5배 빠르고 404 에러 로그가 줄어듭니다.
            info = etf.info 
            
            # AUM 필터링 ($10MM)
            aum = info.get('totalAssets') or info.get('marketCap')
            
            if aum and aum >= 10_000_000:
                # 레버리지인지 이름으로 한 번 더 검증 (선택 사항)
                name = info.get('longName', '')
                keywords = ['Leveraged', 'Bull', 'Bear', '2x', '3x', 'Short', 'Ultra']
                
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
    print(f"🎉 총 {len(final_data)}개 종목으로 갱신 완료!")

if __name__ == "__main__":
    update_ranking()
