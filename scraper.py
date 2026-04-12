import cloudscraper
import pandas as pd
import json
import io

def get_etf_data():
    url = "https://etfdb.com/themes/leveraged-etfs/"
    
    try:
        # 사람의 크롬 브라우저인 것처럼 완벽하게 위장
        scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
        response = scraper.get(url, timeout=30)
        response.raise_for_status()
        
        # 데이터 읽기
        tables = pd.read_html(io.StringIO(response.text))
        df = tables[0]

        # 데이터 가공
        new_df = df.iloc[:, [0, 1, 4]].copy()
        new_df.columns = ['ticker', 'name', 'aum']
        
        new_df['aum'] = new_df['aum'].replace('[\$,]', '', regex=True).astype(float)
        final_df = new_df[new_df['aum'] >= 10].sort_values(by='aum', ascending=False)

        def simplify_desc(row):
            n = str(row['name']).upper()
            t = str(row['ticker']).upper()
            mult = "3배" if "3X" in n else "2배" if "2X" in n or "ULTRA" in n else "레버리지"
            
            mapping = {
                "QQQ": "나스닥100", "SOXL": "반도체", "SOXS": "반도체 인버스",
                "SPY": "S&P500", "VOO": "S&P500", "TSLA": "테슬라", 
                "NVDA": "엔비디아", "GOLD": "금", "MEX": "멕시코", "IND": "인도",
                "TREASURY": "미 국채", "TECHNOLOGY": "기술주", "SMALL CAP": "중소형주"
            }
            
            core = "기타"
            for key, val in mapping.items():
                if key in t or key in n:
                    core = val
                    break
            return f"{row['name']} ({core} {mult})"

        final_df['display_name'] = final_df.apply(simplify_desc, axis=1)
        
        data = final_df[['ticker', 'display_name', 'aum']].to_dict(orient='records')
        
    except Exception as e:
        print(f"⚠️ 데이터 수집 실패: {e}")
        data = [
            {"ticker": "ERROR", "display_name": "웹사이트 보안 차단으로 인해 수집 실패", "aum": 0}
        ]

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_etf_data()
