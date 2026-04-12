import requests
import json

def get_etf_data():
    # 보안이 까다로운 사이트 대신, 비교적 접근이 원활한 데이터 소스를 사용합니다.
    # 주요 레버리지 ETF 리스트 (AUM이 큰 종목 위주로 직접 구성하여 안정성 확보)
    tickers = [
        "TQQQ", "SQQQ", "SOXL", "SOXS", "UPRO", "SPXU", "TNA", "TZA", 
        "FNGU", "FNGD", "BULZ", "BERZ", "LABU", "LABD", "YINN", "YANG",
        "TECL", "TECS", "UVXY", "BITO", "USD", "SSG"
    ]
    
    final_data = []
    
    # 야후 파이낸스 API를 통해 데이터를 가져옵니다 (차단 확률 매우 낮음)
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for ticker in tickers:
        try:
            url = f"https://query1.finance.yahoo.com/v7/finance/options/{ticker}"
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()
            
            # 종목명과 가격 정보를 가져옴 (AUM 대신 시가총액이나 거래대금 지표로 대체 가능하나, 여기선 이름 위주)
            meta = data['optionChain']['result'][0]['quote']
            name = meta.get('longName', meta.get('shortName', ticker))
            
            # 설명 추가 로직
            desc = "3배" if "3X" in name.upper() or "TRIPLE" in name.upper() else "2배"
            if "QQQ" in ticker or "NASDAQ" in name.upper(): category = "나스닥100"
            elif "SEMICONDUCTOR" in name.upper() or "SOX" in ticker: category = "반도체"
            elif "S&P 500" in name.upper() or "SPX" in ticker: category = "S&P500"
            else: category = "레버리지"
            
            final_data.append({
                "ticker": ticker,
                "display_name": f"{name} ({category} {desc})",
                "aum": meta.get('marketCap', 0) / 1000000 # 백만 달러 단위로 변환
            })
        except:
            continue

    # AUM(시가총액) 순으로 정렬
    final_data = sorted(final_data, key=lambda x: x['aum'], reverse=True)

    # 데이터가 아예 없을 경우를 대비한 최소한의 결과
    if not final_data:
        final_data = [{"ticker": "N/A", "display_name": "데이터 업데이트 일시 오류", "aum": 0}]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_etf_data()
