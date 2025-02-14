# AI-ML-Driven Quantitative Trading: Adaptive Signal Optimization for Technical & Hybrid Strategies

## Overview
This project develops a **hybrid quantitative trading strategy** that integrates **technical indicators, risk management, and economic event-based analysis**. The strategy dynamically adapts to market conditions by optimizing **buy/sell signals** based on historical **Sharpe Ratio** and **Win/Loss Ratio**.

## Machine Learning Integration
Our approach leverages **Machine Learning (ML) techniques** to optimize trading signals and enhance decision-making. Specifically:
- **Adaptive Threshold Optimization:** Machine learning models adjust entry/exit points dynamically based on past performance.
- **Feature Engineering:** Extracting key market indicators (e.g., volatility, macroeconomic trends) for better predictive capabilities.
- **Optimization Algorithms:** Utilizing **Bayesian Optimization** and **Grid Search** to fine-tune strategy parameters.
- **Risk Management Models:** Detecting market anomalies using statistical outlier detection methods.

## Data Sources
We collect **financial data** from sources such as **FactSet and Yahoo Finance**, including:
- **Stock Price Data:** Open, close, high, low prices aggregated weekly and monthly.
- **Economic Event Data:** Interest rates (Fed), employment rate, CPI, GDP (announced yearly).

## Trading Strategies
### 1. Technical Analysis-Based Strategy
- Uses **Moving Average (MA)** and **Risk-Based Indicators** (e.g., ATR, VaR, MDD) to generate buy/sell signals.
- Final **Technical Signal:**
  $$
  f_{technical} = w_1 \cdot F_{MA} + w_2 \cdot F_{Risk} \in \{-1, 0, +1\}
  $$

### 2. Hybrid Trading Strategy
- Extends **Technical Analysis** by integrating **Macroeconomic Events** to refine trading decisions.
- Final **Hybrid Signal:**
  $$
  f_{hybrid} = w_1 \cdot F_{MA} + w_2 \cdot F_{Risk} + w_3 \cdot F_{Econ} \in \{-1, 0, +1\}
  $$

## Backtesting & Optimization
The strategy is validated using **backtesting** across multiple timeframes:
- **Short-term (6 months - 1 year)**: Evaluates recent trends.
- **Mid-term (5 years)**: Tests performance across different market cycles.
- **Long-term (10 years)**: Ensures stability under varying economic conditions.

### Optimization Methods:
- **Sharpe Ratio & Win/Loss Ratio Maximization:** Used to refine thresholds and strategy parameters.
- **Bayesian Optimization & Grid Search:** Applied to optimize weights \(w_1, w_2, w_3\) and thresholds.

## Implementation
- **Programming Languages:** Python and R
- **Libraries Used:** Pandas, NumPy, SciPy, TensorFlow, Scikit-learn
- **Deployment:** Jupyter Notebooks for development and experimentation.

## Conclusion & Future Work
This project demonstrates a **data-driven trading strategy** that adapts to market fluctuations using **ML-driven optimization**. Future improvements include exploring **reinforcement learning techniques** for **dynamic strategy adjustments** and expanding **feature engineering methods** for more robust market predictions.
