# ML-Driven Hybrid Quantitative Trading (Proposal)

## Overview
This project develops a **hybrid quantitative trading strategy** that integrates **technical indicators, risk management, and economic event-based analysis**. The strategy dynamically adapts to market conditions by optimizing **buy/sell signals** based on historical **Sharpe Ratio** and **Win/Loss Ratio**.

## Machine Learning Integration
Our approach leverages **Machine Learning (ML) techniques** to optimize trading signals and enhance decision-making. Specifically:
- **Adaptive Probability Scaling:** Each trading component returns a probability score, which is optimized dynamically.
- **Feature Engineering:** Extracting key market indicators (e.g., volatility, macroeconomic trends) for better predictive capabilities.
- **Optimization Algorithms:** Utilizing **Bayesian Optimization** and **Grid Search** to fine-tune probability scaling parameters and decision thresholds.
- **Risk Management Models:** Detecting market anomalies using statistical outlier detection methods.

## Data Sources
We collect **financial data** from sources such as **FactSet and Yahoo Finance**, including:
- **Stock Price Data:** Open, close, high, low prices aggregated weekly and monthly.
- **Economic Event Data:** Interest rates (Fed), employment rate, CPI, GDP (announced yearly).

## Trading Strategies
### 1. Probability-Based Technical Strategy
Instead of fixed signals, each function returns a probability score **P** in the range **[0,1]**, which is optimized dynamically. The final trading signal **f** is determined based on probability outputs:

<img src="https://latex.codecogs.com/png.image?\dpi{110} P_{MA} = \sigma(\lambda_{MA} (Short_{MA} - Long_{MA}))" />

<img src="https://latex.codecogs.com/png.image?\dpi{110} P_{Risk} = \sigma(\lambda_{Risk} (VaR - ATR) + Outlier_{score})" />

where \( \sigma(x) = \frac{1}{1+e^{-x}} \) is the sigmoid function, and \( \lambda_{MA}, \lambda_{Risk} \) are adaptive scaling parameters optimized across multiple timeframes.

**Final Technical Signal:**
<img src="https://latex.codecogs.com/png.image?\dpi{110} f_{technical} = w_1 \cdot P_{MA} + w_2 \cdot P_{Risk}" />

### 2. Probability-Based Hybrid Strategy
We extend **Technical Analysis** by integrating **Macroeconomic Events** to refine trading decisions:

<img src="https://latex.codecogs.com/png.image?\dpi{110} P_{Econ} = \sigma(\lambda_{Econ} (GDP - Interest_{Rate}))" />

**Final Hybrid Signal:**
<img src="https://latex.codecogs.com/png.image?\dpi{110} f_{hybrid} = w_1 \cdot P_{MA} + w_2 \cdot P_{Risk} + w_3 \cdot P_{Econ}" />

The final trading decision follows:
- \( f < -T_{adaptive} \) → **Sell (-1)**
- \( -T_{adaptive} \leq f \leq T_{adaptive} \) → **Hold (0)**
- \( f > T_{adaptive} \) → **Buy (+1)**

where \( T_{adaptive} \) is a dynamically optimized threshold.

## Backtesting & Optimization
The strategy is validated using **backtesting** across multiple timeframes:
- **Short-term (6 months - 1 year)**: Evaluates recent trends.
- **Mid-term (5 years)**: Tests performance across different market cycles.
- **Long-term (10 years)**: Ensures stability under varying economic conditions.

### Optimization Methods:
- **Probability Scaling Optimization:** Finding the most stable probability scaling parameters \( \lambda \).
- **Threshold Optimization:** Dynamically tuning \( T_{adaptive} \) to maximize Sharpe Ratio and Win/Loss Ratio.
- **Bayesian Optimization & Grid Search:** Applied to optimize weights \( w_1, w_2, w_3 \) and thresholds.

## Implementation
- **Programming Languages:** Python and R
- **Libraries Used:** Pandas, NumPy, SciPy, TensorFlow, Scikit-learn
- **Deployment:** Jupyter Notebooks for development and experimentation.

## Conclusion & Future Work
This project demonstrates a **data-driven trading strategy** that adapts to market fluctuations using **ML-driven optimization**. Future improvements include:
- **Exploring reinforcement learning techniques** for dynamic strategy adjustments.
- **Expanding feature engineering** for more robust market predictions.
- **Testing additional ML-based optimization techniques** such as evolutionary algorithms.

---

📈 **This project aims to bridge ML and quantitative trading for improved decision-making and risk management! 🚀**
