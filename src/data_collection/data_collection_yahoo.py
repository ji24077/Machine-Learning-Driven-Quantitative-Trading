import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# 프로젝트 루트 경로 찾기
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
# 데이터 경로 생성
data_path = os.path.join(project_root, 'data', 'raw')
os.makedirs(data_path, exist_ok=True)

# 수집할 주식 목록 (문서에서 언급된 주식들)
stocks = ['SOXL', 'NVDA', 'XOM']

# 데이터 수집 기간 설정 (10년 데이터)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# 주식별 데이터 수집 및 저장
for stock in stocks:
    print(f"{stock} 데이터 수집 중...")
    
    # 일별 데이터 수집
    daily_data = yf.download(stock, start=start_date, end=end_date, interval='1d')
    
    # 주별 데이터 수집
    weekly_data = yf.download(stock, start=start_date, end=end_date, interval='1wk')
    
    # 월별 데이터 수집
    monthly_data = yf.download(stock, start=start_date, end=end_date, interval='1mo')
    
    # Excel 파일로 저장
    with pd.ExcelWriter(os.path.join(data_path, f'{stock}_data.xlsx')) as writer:
        daily_data.to_excel(writer, sheet_name='Daily')
        weekly_data.to_excel(writer, sheet_name='Weekly')
        monthly_data.to_excel(writer, sheet_name='Monthly')
    
    print(f"{stock} 데이터 저장 완료: {os.path.join(data_path, f'{stock}_data.xlsx')}")

# 경제 지표 데이터 수집 (Yahoo Finance에서 가능한 것들)
# GDP, 인플레이션 등의 데이터는 다른 소스가 필요할 수 있음
economic_indicators = [
    '^TNX',  # 10-Year Treasury Yield
    '^VIX',  # Volatility Index
]

# 경제 지표 데이터 수집 및 저장
for indicator in economic_indicators:
    print(f"{indicator} 데이터 수집 중...")
    
    # 일별 데이터 수집
    indicator_data = yf.download(indicator, start=start_date, end=end_date, interval='1d')
    
    # Excel 파일로 저장
    indicator_name = indicator.replace('^', '')
    indicator_data.to_excel(os.path.join(data_path, f'{indicator_name}_data.xlsx'))
    
    print(f"{indicator} 데이터 저장 완료: {os.path.join(data_path, f'{indicator_name}_data.xlsx')}")

print("모든 데이터 수집 완료!") 