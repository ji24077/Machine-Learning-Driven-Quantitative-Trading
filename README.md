# Machine Learning Driven Quantitative Trading

이 프로젝트는 기술적 지표, 리스크 관리, 그리고 경제 이벤트 기반 분석을 통합한 하이브리드 트레이딩 전략을 개발합니다. 과거 Sharpe Ratio와 Win/Loss Ratio를 기반으로 파라미터를 동적으로 조정하여 다양한 시장 상황에서 수익성과 안정성을 최적화하는 것을 목표로 합니다.

## 프로젝트 구조

```
Machine-Learning-Driven-Quantitative-Trading/
├── data/
│   ├── raw/             # 원본 데이터 저장
│   └── processed/       # 전처리된 데이터 저장
├── src/
│   ├── data_collection/ # 데이터 수집 관련 코드
│   │   ├── __init__.py
│   │   ├── data_collection_yahoo.py  # Yahoo Finance 데이터 수집
│   │   └── data_collection_fred.py   # FRED 경제 지표 데이터 수집
│   ├── data_processing/ # 데이터 처리 관련 코드
│   │   ├── __init__.py
│   │   └── data_preprocessing.py     # 데이터 전처리
│   └── main.py          # 메인 실행 스크립트
└── requirements.txt     # 필요한 패키지 목록
```

## 설치 방법

1. 필요한 패키지 설치:

```bash
pip install -r requirements.txt
```

2. FRED API 키 발급:
   - [FRED API 키 발급 페이지](https://fred.stlouisfed.org/docs/api/api_key.html)에서 API 키를 발급받습니다.

## 사용 방법

### 데이터 수집 및 전처리

다음 명령어로 데이터 수집 및 전처리를 실행합니다:

```bash
python src/main.py
```

이 스크립트는 다음 작업을 수행합니다:
1. Yahoo Finance에서 주식 데이터 수집 (SOXL, NVDA, XOM)
2. FRED에서 경제 지표 데이터 수집 (GDP, CPI, 실업률, 연방기금금리 등)
3. 수집된 데이터 전처리 (정규화, 이상치 처리 등)

### 개별 스크립트 실행

각 스크립트를 개별적으로 실행할 수도 있습니다:

```bash
# Yahoo Finance에서 주식 데이터 수집
python src/data_collection/data_collection_yahoo.py

# FRED에서 경제 지표 데이터 수집 (API 키 필요)
python src/data_collection/data_collection_fred.py

# 데이터 전처리
python src/data_processing/data_preprocessing.py
```

## 데이터 설명

### 주식 데이터
- 일별, 주별, 월별 데이터 포함
- 각 데이터는 Open, High, Low, Close, Volume 정보 포함
- 전처리 후 이동평균, 정규화된 가격, 이상치 점수 등 추가

### 경제 지표 데이터
- GDP, CPI, 실업률, 연방기금금리, 고용 등 포함
- 각 지표는 정규화된 값으로도 제공

## 참고 사항

- FRED API 키가 없어도 Yahoo Finance 데이터는 수집 가능합니다.
- 데이터 수집 기간은 기본적으로 10년으로 설정되어 있습니다.
- 이상치는 제거하지 않고 이상치 점수로 변환하여 리스크 함수에 통합합니다.

# ML-Driven Hybrid Quantitative Trading Strategy 🚀

## Overview
This project develops a **hybrid quantitative trading strategy** that integrates **technical indicators, risk management, and economic event-based analysis**. The strategy dynamically adapts to market conditions by optimizing **buy/sell signals** based on historical **Sharpe Ratio** and **Win/Loss Ratio**. 

Instead of using fixed signals, each function returns a **probability score** in the range **[0,1]**, which is optimized dynamically. The final decision is based on an adaptive threshold.

- **-1 (Sell):** Strong bearish signal  
- **0 (Hold):** Neutral or uncertain market condition  
- **+1 (Buy):** Strong bullish signal  

---

## 📊 Machine Learning Integration
We incorporate **Machine Learning (ML) techniques** to optimize trading signals and improve decision-making. Our model includes:

- **Adaptive Probability Scaling:** Instead of discrete signals, each trading component returns a probability score optimized dynamically.
- **Feature Engineering:** Extracting market indicators (volatility, macroeconomic trends) for better predictive capabilities.
- **Optimization Algorithms:** Utilizing **Bayesian Optimization** and **Grid Search** to fine-tune probability scaling parameters and decision thresholds.
- **Risk Management Models:** Detecting market anomalies using **statistical outlier detection** and **volatility-based risk modeling**.

---

## 📌 Data Sources
We collect financial data from sources like **FactSet and Yahoo Finance**, including:

- **Stock Price Data:** Open, close, high, low prices aggregated **weekly** and **monthly**.
- **Economic Event Data:** Interest rates (Fed), employment rate, CPI, GDP (announced yearly).
- **Market Risk Metrics:** VaR (Value at Risk), ATR (Average True Range), extreme outlier detection.

---

## 📈 Trading Strategies
### **1️⃣ Probability-Based Technical Trading Strategy**
Instead of fixed signals, we estimate the probability of **bullish** or **bearish** market conditions.

$$ P_{MA} = \sigma(\lambda_{MA} (Short_{MA} - Long_{MA})) $$

$$ P_{Risk} = \sigma(\lambda_{Risk} (VaR - ATR) + Outlier_{score}) $$

Where:

$$ \sigma(x) = \frac{1}{1+e^{-x}} $$ 

$$  \lambda_{MA}, \lambda_{Risk} =  adjusted \ dynamically $$ 

**Final Technical Signal:**

$$ f_{technical} = w_1 \cdot P_{MA} + w_2 \cdot P_{Risk} $$

---

### **2️⃣ Probability-Based Hybrid Trading Strategy**
We extend **Technical Analysis** by integrating **Macroeconomic Events** to refine trading decisions.

$$ P_{Econ} = \sigma(\lambda_{Econ} (GDP - Interest_{Rate})) $$

**Final Hybrid Signal:**

$$ f_{hybrid} = w_1 \cdot P_{MA} + w_2 \cdot P_{Risk} + w_3 \cdot P_{Econ} $$

The final trading decision follows:

- \( f < -T_{adaptive} \) → **Sell (-1)**
- \( -T_{adaptive} \leq f \leq T_{adaptive} \) → **Hold (0)**
- \( f > T_{adaptive} \) → **Buy (+1)**

Where **\( T_{adaptive} \)** is a **dynamically optimized threshold**.

---

## 🏆 Backtesting & Adaptive Threshold Optimization
All probability outputs are compared to **adaptive thresholds \( T_{adaptive} \)**, which are optimized based on **Sharpe Ratio and Win/Loss Ratio**.

$$ T_{adaptive} = \arg\max_T Sharpe(T) + Win/Loss(T) $$

Backtesting is conducted over **multiple timeframes** to ensure robust optimization:

- **Short-term (6 months - 1 year):** Evaluates recent trends.
- **Mid-term (5 years):** Tests performance across different market cycles.
- **Long-term (10 years):** Ensures stability under varying economic conditions.

---

## 🔧 Optimization Methods
We optimize both **probability scaling parameters (\(\lambda\))** and **decision thresholds** to ensure stability across different market conditions.

- **Bayesian Optimization:** Finds the most stable probability thresholds and \(\lambda\) values across multiple timeframes.
- **Grid Search:** Ensures robustness by systematically testing different threshold and \(\lambda\) ranges.
- **Timeframe-Aware Optimization:** We compare optimized \(\lambda\) values across different timeframes and select the most stable configuration that maximizes **Sharpe Ratio and Win/Loss Ratio**.

---

## 🚀 Implementation Details
- **Programming Languages:** Python and R
- **Libraries Used:** Pandas, NumPy, SciPy, TensorFlow, Scikit-learn
- **Optimization Techniques:** Bayesian Optimization, Grid Search, Sharpe Ratio maximization
- **Deployment:** Jupyter Notebooks for development and experimentation.

---

## 📌 Conclusion & Future Work
This project demonstrates a **data-driven trading strategy** that adapts to market fluctuations using **ML-driven optimization**. Future improvements include:

- **Exploring Reinforcement Learning** to enhance adaptive decision-making.
- **Expanding Feature Engineering** for improved financial predictions.
- **Testing Alternative ML Optimization Techniques** (e.g., evolutionary algorithms, deep learning models).

---

## 📌 References
1. Machine Learning for Asset Management – Marcos López de Prado
2. Quantitative Trading Strategies – Ernest Chan
3. Bayesian Optimization for Financial Markets – Research Papers from arXiv
4. FactSet & Yahoo Finance API Documentation

🔥 **This project bridges ML and quantitative trading for more adaptive, data-driven investment decisions! 🚀**  
