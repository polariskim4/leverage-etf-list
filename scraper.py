import requests
import pandas as pd
import json

def get_etf_data():
    url = "https://etfdb.com/themes/leveraged-etfs/"
    # 브라우저인 척 속여서 차단을 방지하는 헤더입니다.
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        # 테이블을 읽어옵니다.
        tables = pd.read_html(response.text)
        df = tables[0]

        # 컬럼 이름이 유동적일 수 있으므로 순서로 접근합니다.
        # 보통 0:Symbol, 1:ETF Name, 4:Assets
        new_df = df.iloc[:, [0, 1, 4]].copy()
        new_df.columns = ['ticker', 'name', 'aum']
        
        # AUM 숫자 변환 ($12,345.67 -> 12345.67)
        new_df['aum'] = new_df['aum'].replace('[\$,]', '', regex=True).astype(float)

        # $10MM 이상 필터링
        new_df = new_df[new_df['aum'] >= 10].sort_values(by='aum', ascending=False)

        # 간단한 설명 추가
        def add_desc(row):
            n, t = row['name'].upper(), row['ticker'].upper()
            m = "3배" if "3X" in n else "2배" if ("2X" in n or "ULTRA" in n) else "레버리지"
            if "QQQ" in t or "NASDAQ" in n: d = f"나스닥100 {m}"
            elif "S&P 500" in n or "SPX" in t: d = f"S&P500 {m}"
            elif "SEMICONDUCTOR" in n: d = f"반도체 {m}"
            elif "GOLD" in n: d = f"금 {m}"
            elif "INDIA" in n: d = f"인도 {m}"
            elif "MEXICO" in n: d = f"멕시코 {m}"
            else: d = f"{m}"
            return f"({d})"

        new_df['desc'] = new_df.apply(add_desc, axis=1)
        new_df['display_name'] = new_df['name'] + " " + new_df['desc']

        # 저장
        result = new_df[['ticker', 'display_name', 'aum']].to_dict(orient='records')
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print("Successfully saved data.json")

    except Exception as e:
        print(f"Error occurred: {e}")
        exit(1) # 에러 발생 시 강제 종료해서 Actions에 알림

if __name__ == "__main__":
    get_etf_data()
