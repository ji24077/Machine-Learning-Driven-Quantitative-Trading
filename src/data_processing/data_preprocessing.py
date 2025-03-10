import pandas as pd
import numpy as np
import os
# from scipy import stats  # SciPy 대신 NumPy 사용
import glob

# 데이터 디렉토리 설정
raw_data_dir = 'data/raw'
processed_data_dir = 'data/processed'

# 처리된 데이터 저장 디렉토리 생성
os.makedirs(processed_data_dir, exist_ok=True)

def detect_outliers(series, threshold=3):
    """
    Z-score 방식으로 이상치 탐지 (NumPy 사용)
    
    Args:
        series: 데이터 시리즈
        threshold: Z-score 임계값 (기본값: 3)
    
    Returns:
        이상치 여부를 나타내는 불리언 마스크
    """
    series_no_nan = series.dropna()
    mean = np.mean(series_no_nan)
    std = np.std(series_no_nan)
    z_scores = np.abs((series_no_nan - mean) / std) if std > 0 else np.zeros_like(series_no_nan)
    return z_scores > threshold

def calculate_outlier_score(series):
    """
    이상치 점수 계산 (Z-score 기반, NumPy 사용)
    
    Args:
        series: 데이터 시리즈
    
    Returns:
        이상치 점수
    """
    series_no_nan = series.dropna()
    mean = np.mean(series_no_nan)
    std = np.std(series_no_nan)
    
    if std > 0:
        z_scores = np.abs((series_no_nan - mean) / std)
        # Z-score를 0-1 범위로 정규화
        min_z = np.min(z_scores)
        max_z = np.max(z_scores)
        outlier_scores = (z_scores - min_z) / (max_z - min_z) if max_z > min_z else z_scores
    else:
        outlier_scores = np.zeros_like(series_no_nan)
    
    return pd.Series(outlier_scores, index=series_no_nan.index)

def normalize_price_movements(df):
    """
    가격 움직임 정규화
    
    Args:
        df: 주가 데이터 DataFrame
    
    Returns:
        정규화된 가격 데이터가 추가된 DataFrame
    """
    # 숫자 열 확인 및 변환
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    for col in numeric_columns:
        if col in df.columns:
            # 문자열을 숫자로 변환 (쉼표 제거 후 변환)
            if df[col].dtype == 'object':
                try:
                    df[col] = df[col].replace({',': ''}, regex=True).astype(float)
                except Exception as e:
                    print(f"  경고: {col} 열을 숫자로 변환할 수 없습니다. 오류: {e}")
    
    # 수익률 계산
    if 'Close' in df.columns and df['Close'].dtype != 'object':
        df['Returns'] = df['Close'].pct_change(fill_method=None)
        
        # 정규화된 가격 (0-1 범위)
        min_price = df['Close'].min()
        max_price = df['Close'].max()
        if max_price > min_price:
            df['NormalizedPrice'] = (df['Close'] - min_price) / (max_price - min_price)
        
        # 이동평균 계산
        df['MA_5'] = df['Close'].rolling(window=5).mean()
        df['MA_20'] = df['Close'].rolling(window=20).mean()
        df['MA_50'] = df['Close'].rolling(window=50).mean()
        
        # 변동성 계산 (ATR 간소화 버전)
        if 'High' in df.columns and 'Low' in df.columns:
            df['Volatility'] = df['High'] - df['Low']
            
            # 이상치 점수 계산
            if 'Returns' in df.columns:
                returns_outlier_score = calculate_outlier_score(df['Returns'])
                df.loc[returns_outlier_score.index, 'ReturnsOutlierScore'] = returns_outlier_score
            
            if 'Volatility' in df.columns:
                volatility_outlier_score = calculate_outlier_score(df['Volatility'])
                df.loc[volatility_outlier_score.index, 'VolatilityOutlierScore'] = volatility_outlier_score
    else:
        print("  경고: 'Close' 열이 없거나 숫자 형식이 아닙니다. 일부 지표를 계산할 수 없습니다.")
    
    # 결측값 처리
    df.fillna(method='ffill', inplace=True)
    df.fillna(method='bfill', inplace=True)
    
    return df

# 주식 데이터 전처리
stock_files = glob.glob(f"{raw_data_dir}/*_data.xlsx")
for file_path in stock_files:
    stock_name = os.path.basename(file_path).split('_')[0]
    print(f"{stock_name} 데이터 전처리 중...")
    
    try:
        # Excel 파일에서 데이터 읽기
        with pd.ExcelFile(file_path) as xls:
            # 각 시간대별 데이터 처리
            for sheet_name in xls.sheet_names:
                print(f"  {sheet_name} 시트 처리 중...")
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # 데이터 구조 확인
                print(f"  열 목록: {df.columns.tolist()}")
                print(f"  데이터 타입: {df.dtypes}")
                
                # 인덱스가 날짜 형식인지 확인
                if not isinstance(df.index, pd.DatetimeIndex) and 'Date' in df.columns:
                    df.set_index('Date', inplace=True)
                
                # 데이터 전처리
                processed_df = normalize_price_movements(df)
                
                # 처리된 데이터 저장
                output_file = f"{processed_data_dir}/{stock_name}_{sheet_name.lower()}_processed.csv"
                processed_df.to_csv(output_file)
                print(f"  {sheet_name} 데이터 처리 완료: {output_file}")
    except Exception as e:
        print(f"  오류: {stock_name} 데이터 처리 중 오류 발생: {e}")

# 경제 지표 데이터 전처리
economic_file = f"{raw_data_dir}/economic_indicators.xlsx"
if os.path.exists(economic_file):
    print("경제 지표 데이터 전처리 중...")
    
    try:
        # Excel 파일에서 데이터 읽기
        economic_df = pd.read_excel(economic_file, index_col=0)
        
        # 결측값 처리
        economic_df.fillna(method='ffill', inplace=True)
        
        # 각 지표 정규화
        for column in economic_df.columns:
            # 문자열을 숫자로 변환
            if economic_df[column].dtype == 'object':
                try:
                    economic_df[column] = economic_df[column].replace({',': ''}, regex=True).astype(float)
                except:
                    print(f"  경고: {column} 열을 숫자로 변환할 수 없습니다.")
                    continue
            
            min_val = economic_df[column].min()
            max_val = economic_df[column].max()
            if max_val > min_val:
                economic_df[f"{column}_Normalized"] = (economic_df[column] - min_val) / (max_val - min_val)
        
        # 처리된 데이터 저장
        output_file = f"{processed_data_dir}/economic_indicators_processed.csv"
        economic_df.to_csv(output_file)
        print(f"경제 지표 데이터 처리 완료: {output_file}")
    except Exception as e:
        print(f"오류: 경제 지표 데이터 처리 중 오류 발생: {e}")

print("모든 데이터 전처리 완료!") 