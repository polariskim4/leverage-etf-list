import yfinance as yf
import json
import time
import requests

def get_leveraged_etf_list():
    """레버리지 ETF 후보군을 넓게 탐색합니다."""
    # 대표적인 레버리지 운용사 및 키워드 기반 확장 리스트
    # 실제 '모든' 종목을 API 없이 찾기 위해 가장 점유율이 높은 티커들과 
    # 레버리지 ETF 전문 운용사(ProShares, Direxion 등)의 주요 종목을 포함합니다.
    base_tickers = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "UPRO", "SPXU", "FNGU", "FNGD", "TNA", "TZA",
        "BULZ", "BERZ", "LABU", "LABD", "YINN", "YANG", "TECL", "TECS", "BITO", "USD",
        "QLD", "QID", "SSO", "SDS", "UWM", "TWM", "DIG", "DUG", "UYG", "SKF",
        "FAS", "FAZ", "ERX", "ERY", "GUSH", "DRIP", "DFEN", "NUGT", "DUST", "CURE",
        "TECS", "TECL", "SCO", "UCO", "BOIL", "KOLD", "SVXY", "UVXY", "YCL", "YCS"
    ]
    
    # 팁: 야후 파이낸스에서 'Leveraged' 카테고리를 직접 긁어오는 것은 차단 위험이 커서
    # 신뢰도 높은 광범위 리스트를 순회하며 AUM 필터링을 거치는 것이 가장 안정적입니다.
    
    final_data = []
    print(f"📡 시장 데이터 분석 및 $10MM 이상 종목 필터링 시작...")

    for ticker in base_tickers:
        try:
            etf = yf.Ticker(ticker)
            info = etf.info
            
            # AUM 정보 정밀 추출 (totalAssets -> navPrice * share -> marketCap 순서)
            aum = info.get('totalAssets') or info.get('marketCap')
            
            # AUM이 $10,000,000 (10MM) 이상인 것만 선별
            if aum and aum >= 10_000_000:
                name = info.get('longName', ticker)
                # 'Leveraged', 'Bull', 'Bear', '2x', '3x' 등 키워드 확인 (선택 사항)
                
                final_data.append({
                    "ticker": ticker,
                    "display_name": name,
                    "aum": round(aum / 1_000_000, 2) # Million 달러 단위
                })
                print(f"✅ {ticker} ($ {round(aum/1_000_000, 1)} MM) 추가")
            
            time.sleep(0.3)
        except Exception as e:
            continue

    # AUM 기준 내림차순 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)
    print(f"🎉 총 {len(final_data)}개의 레버리지 ETF 데이터 갱신 완료!")

if __name__ == "__main__":
    get_leveraged_etf_list()
