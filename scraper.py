import requests
import pandas as pd
import json
import io

def get_etf_data():
    url = "https://etfdb.com/themes/leveraged-etfs/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }
    
    try:
        # 1. 사이트 접속
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status() # 접속 실패 시 에러 발생
        
        # 2. 데이터 읽기 (pd.read_html 대신 StringIO 사용으로 안정성 강화)
        tables = pd.read_html(io.StringIO(response.text))
        df = tables[0]

        # 3. 데이터 가공
        # 컬럼 이름이 바뀌어도 대응하도록 위치(iloc)로 선택
        new_df = df.iloc[:, [0, 1, 4]].copy()
        new_df.columns = ['ticker', 'name', 'aum']
        
        # AUM 수치화
        new_df['aum'] = new_df['aum'].replace('[\$,]', '', regex=True).astype(float)
        
        # $10MM 이상 필터링
        final_df = new_df[new_df['aum'] >= 10].sort_values(by='aum', ascending=False)

        # 종목명 정리 및 설명 추가
        def simplify_desc(row):
            n = row['name'].upper()
            t = row['ticker'].upper()
            mult = "3배" if "3X" in n else "2배" if "2X" in n or "ULTRA" in n else ""
            
            mapping = {
                "QQQ": "나스닥100", "SOXL": "반도체", "SOXS": "반도체 인버스",
                "SPY": "S&P500", "VOO": "S&P500", "TSLA": "테슬라", 
                "NVDA": "엔비디아", "GOLD": "금", "MEX": "멕시코", "IND": "인도"
            }
            
            core = "레버리지"
            for key, val in mapping.items():
                if key in t or key in n:
                    core = val
                    break
            return f"{row['name']} ({core} {mult})"

        final_df['display_name'] = final_df.apply(simplify_desc, axis=1)
        
        # 4. JSON 저장
        data = final_df[['ticker', 'display_name', 'aum']].to_dict(orient='records')
        
    except Exception as e:
        print(f"⚠️ 실시간 데이터 수집 실패: {e}")
        # 접속 실패 시 보여줄 최소한의 백업 데이터 (빈 화면 방지)
        data = [
            {"ticker": "TQQQ", "display_name": "ProShares UltraPro QQQ (나스닥100 3배) - 점검중", "aum": 25000.0},
            {"ticker": "SOXL", "display_name": "Direxion Semiconductor Bull 3X (반도체 3배) - 점검중", "aum": 12000.0}
        ]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_etf_data()
