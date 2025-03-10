"""
데이터 수집 모듈

이 패키지는 다양한 소스에서 데이터를 수집하는 기능을 제공합니다.
- Yahoo Finance에서 주식 데이터 수집
- FRED에서 경제 지표 데이터 수집
"""

from .data_collection_yahoo import *
from .data_collection_fred import * 