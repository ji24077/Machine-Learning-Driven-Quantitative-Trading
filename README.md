# Machine Learning Driven Quantitative Trading

This project develops a hybrid trading strategy that integrates technical indicators, risk management, and economic event-based analysis. By dynamically adapting parameters based on historical Sharpe Ratio and Win/Loss Ratio, our approach aims to maximize profitability while ensuring stability across different market conditions.

## Project Structure

```
Machine-Learning-Driven-Quantitative-Trading/
├── data/
│   ├── raw/             # Raw data storage
│   └── processed/       # Processed data storage
├── src/
│   ├── data_collection/ # Data collection code
│   │   ├── __init__.py
│   │   ├── data_collection_yahoo.py  # Yahoo Finance data collection
│   │   └── data_collection_fred.py   # FRED economic indicators collection
│   ├── data_processing/ # Data processing code
│   │   ├── __init__.py
│   │   └── data_preprocessing.py     # Data preprocessing
│   └── main.py          # Main execution script
└── requirements.txt     # Required packages
```

## Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Get FRED API key:
   - Get your API key from [FRED API Key Page](https://fred.stlouisfed.org/docs/api/api_key.html)

## Usage

### Data Collection and Preprocessing

Run the following command to collect and preprocess data:

```bash
python src/main.py
```

This script performs the following tasks:
1. Collect stock data from Yahoo Finance (SOXL, NVDA, XOM)
2. Collect economic indicators from FRED (GDP, CPI, unemployment rate, federal funds rate, etc.)
3. Preprocess collected data (normalization, outlier handling, etc.)

### Running Individual Scripts

You can also run each script individually:

```bash
# Collect stock data from Yahoo Finance
python src/data_collection/data_collection_yahoo.py

# Collect economic indicators from FRED (API key required)
python src/data_collection/data_collection_fred.py

# Preprocess data
python src/data_processing/data_preprocessing.py
```

## Data Description

### Stock Data
- Includes daily, weekly, and monthly data
- Each dataset contains Open, High, Low, Close, Volume information
- After preprocessing, moving averages, normalized prices, outlier scores, etc. are added

### Economic Indicators
- Includes GDP, CPI, unemployment rate, federal funds rate, employment, etc.
- Each indicator is also provided as normalized values

## Notes

- Yahoo Finance data can be collected without a FRED API key
- Data collection period is set to 10 years by default
- Outliers are not removed but converted to outlier scores and integrated into the risk function

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
