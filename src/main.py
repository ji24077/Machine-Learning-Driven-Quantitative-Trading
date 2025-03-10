"""
메인 실행 스크립트

이 스크립트는 데이터 수집 및 처리 과정을 실행합니다.
"""

import os
import subprocess
import time

def run_script(script_path, description):
    """
    Python 스크립트를 실행하는 함수
    
    Args:
        script_path: 실행할 스크립트 파일 경로
        description: 스크립트 설명
    """
    print(f"\n{'='*80}")
    print(f"실행: {description}")
    print(f"{'='*80}")
    
    try:
        subprocess.run(['python', script_path], check=True)
        print(f"\n{description} 완료!")
    except subprocess.CalledProcessError as e:
        print(f"\n{description} 실패: {e}")
        return False
    
    return True

def main():
    """
    데이터 수집 및 전처리 스크립트를 순차적으로 실행
    """
    # 데이터 디렉토리 생성
    os.makedirs('data/raw', exist_ok=True)
    os.makedirs('data/processed', exist_ok=True)
    
    # 1. Yahoo Finance에서 주식 데이터 수집
    if not run_script('src/data_collection/data_collection_yahoo.py', 'Yahoo Finance에서 주식 데이터 수집'):
        print("주식 데이터 수집 실패. 프로그램을 종료합니다.")
        return
    
    # 2. FRED에서 경제 지표 데이터 수집
    print("\nFRED API 키가 필요합니다.")
    print("FRED API 키를 발급받으셨나요? (Y/N)")
    has_api_key = input().strip().upper()
    
    if has_api_key == 'Y':
        api_key = input("FRED API 키를 입력하세요: ").strip()
        
        # API 키 업데이트
        with open('src/data_collection/data_collection_fred.py', 'r') as file:
            content = file.read()
        
        content = content.replace("fred_api_key = '793c594fd13b09a517072cc115c1421e'", f"fred_api_key = '{api_key}'")
        
        with open('src/data_collection/data_collection_fred.py', 'w') as file:
            file.write(content)
        
        if not run_script('src/data_collection/data_collection_fred.py', 'FRED에서 경제 지표 데이터 수집'):
            print("경제 지표 데이터 수집 실패. 주식 데이터만 전처리합니다.")
    else:
        print("FRED API 키 없이 계속합니다. 경제 지표 데이터는 수집되지 않습니다.")
    
    # 3. 데이터 전처리
    if not run_script('src/data_processing/data_preprocessing.py', '수집된 데이터 전처리'):
        print("데이터 전처리 실패. 프로그램을 종료합니다.")
        return
    
    print("\n모든 데이터 수집 및 전처리가 완료되었습니다!")
    print("데이터는 다음 위치에 저장되었습니다:")
    print(f"  - 원본 데이터: {os.path.abspath('data/raw')}")
    print(f"  - 처리된 데이터: {os.path.abspath('data/processed')}")

if __name__ == "__main__":
    main() 