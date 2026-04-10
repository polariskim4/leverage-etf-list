import requests
import pandas as pd
import json

def get_etf_data():
    url = "https://etfdb.com/themes/leveraged-etfs/"
    headers = {"User-Agent": "Mozilla/5.0"} # 차단 방지용
    
    # 1. 테이블 데이터 읽기
    response = requests.get(url, headers=headers)
    tables = pd.read_html(response.text)
    df = tables[0]

    # 2. 필요한 컬럼 정리 및 AUM 수치화
    # 컬럼명은 사이트 상황에 따라 'Assets' 또는 'Assets ($MM)'일 수 있음
    df = df[['Symbol', 'ETF Name', 'Total Assets ($MM)']]
    df.columns = ['ticker', 'name', 'aum']
    
    # '$12,345.60' -> 12345.60 변환
    df['aum'] = df['aum'].replace('[\$,]', '', regex=True).astype(float)

    # 3. $10MM 이상만 필터링
    df = df[df['aum'] >= 10].sort_values(by='aum', ascending=False)

    # 4. 한글 설명 추가 로직 (키워드 매칭)
    def add_desc(row):
        name = row['name'].upper()
        ticker = row['ticker'].upper()
        desc = ""
        if "3X" in name: mult = "3배"
        elif "2X" in name or "ULTRA" in name: mult = "2배"
        else: mult = "레버리지"
        
        if "QQQ" in ticker or "NASDAQ" in name: desc = f"나스닥100 {mult}"
        elif "S&P 500" in name or "SPX" in ticker: desc = f"S&P500 {mult}"
        elif "SEMICONDUCTOR" in name: desc = f"반도체 {mult}"
        elif "TECHNOLOGY" in name: desc = f"기술주 {mult}"
        elif "TREASURY" in name: desc = f"미 국채 {mult}"
        elif "GOLD" in name: desc = f"금 {mult}"
        elif "INDIA" in name: desc = f"인도 {mult}"
        elif "MEXICO" in name: desc = f"멕시코 {mult}"
        elif "EUROPE" in name: desc = f"유럽 {mult}"
        else: desc = f"기타 {mult}"
        return f"{row['name']} ({desc})"

    df['display_name'] = df.apply(add_desc, axis=1)

    # 5. JSON 저장
    result = df.to_dict(orient='records')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    get_etf_data()
