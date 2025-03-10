import pandas as pd
import os
from fredapi import Fred
from datetime import datetime, timedelta

# 데이터 저장 디렉토리 생성
os.makedirs('data/raw', exist_ok=True)

# FRED API 키 설정
fred_api_key = '793c594fd13b09a517072cc115c1421e'  # API 키 설정 완료

# FRED API 초기화
try:
    fred = Fred(api_key=fred_api_key)
    print("FRED API 연결 성공")
except Exception as e:
    print(f"FRED API 연결 실패: {e}")
    print("API 키를 발급받아 스크립트에 입력해주세요.")
    exit(1)

# 수집할 경제 지표 목록 (문서에서 언급된 지표들)
economic_indicators = {
    'GDP': 'GDP',                  # 실질 GDP
    'CPIAUCSL': 'CPI',             # 소비자 물가 지수
    'UNRATE': 'Unemployment',      # 실업률
    'FEDFUNDS': 'FedRate',         # 연방기금금리
    'PAYEMS': 'Employment',        # 비농업 고용
    'INDPRO': 'IndustrialProduction',  # 산업생산지수
}

# 데이터 수집 기간 설정 (10년 데이터)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# 모든 경제 지표 데이터를 저장할 DataFrame
all_economic_data = pd.DataFrame()

# 경제 지표별 데이터 수집 및 저장
for series_id, indicator_name in economic_indicators.items():
    print(f"{indicator_name} 데이터 수집 중...")
    
    try:
        # FRED에서 데이터 수집
        data = fred.get_series(series_id, start_date, end_date)
        
        # 데이터 이름 변경
        data.name = indicator_name
        
        # 전체 데이터프레임에 추가
        if all_economic_data.empty:
            all_economic_data = pd.DataFrame(data)
        else:
            all_economic_data = pd.concat([all_economic_data, pd.DataFrame(data)], axis=1)
        
        print(f"{indicator_name} 데이터 수집 완료")
    except Exception as e:
        print(f"{indicator_name} 데이터 수집 실패: {e}")

# 모든 경제 지표 데이터를 하나의 Excel 파일로 저장
if not all_economic_data.empty:
    all_economic_data.to_excel('data/raw/economic_indicators.xlsx')
    print("모든 경제 지표 데이터 저장 완료: data/raw/economic_indicators.xlsx")
else:
    print("수집된 경제 지표 데이터가 없습니다.")

print("경제 지표 데이터 수집 완료!") 