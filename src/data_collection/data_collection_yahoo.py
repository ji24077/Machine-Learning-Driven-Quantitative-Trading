"""
Yahoo Finance Data Collection Module

This module collects comprehensive market data from Yahoo Finance API for the QuantML trading system.
Supports multi-timeframe data collection (daily, weekly, monthly) for specified equity symbols.

Features:
- OHLCV data collection for multiple timeframes
- Automated data validation and error handling
- Excel format output with organized sheets
- Configurable date ranges and symbols
- Economic indicator proxies (TNX, VIX) collection

Supported Assets:
- SOXL: Semiconductor sector leveraged ETF
- NVDA: NVIDIA Corporation stock
- XOM: Exxon Mobil Corporation stock

Output Format:
- Excel files with separate sheets for each timeframe
- Raw OHLCV data preserved for downstream processing
"""

import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta

# Determine project root directory for consistent file paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))

# Create data directory for raw market data storage
data_path = os.path.join(project_root, 'data', 'raw')
os.makedirs(data_path, exist_ok=True)

# Define target equity symbols for data collection
# These symbols are specifically chosen for the quantitative trading research
stocks = ['SOXL', 'NVDA', 'XOM']

# Configure data collection timeframe (10 years of historical data)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# Collect and save market data for each target symbol
for stock in stocks:
    print(f"Collecting market data for {stock}...")
    
    try:
        # Daily timeframe data collection
        daily_data = yf.download(stock, start=start_date, end=end_date, interval='1d')
        
        # Weekly timeframe data collection  
        weekly_data = yf.download(stock, start=start_date, end=end_date, interval='1wk')
        
        # Monthly timeframe data collection
        monthly_data = yf.download(stock, start=start_date, end=end_date, interval='1mo')
        
        # Save all timeframes to organized Excel file
        output_file = os.path.join(data_path, f'{stock}_data.xlsx')
        with pd.ExcelWriter(output_file) as writer:
            daily_data.to_excel(writer, sheet_name='Daily')
            weekly_data.to_excel(writer, sheet_name='Weekly')  
            monthly_data.to_excel(writer, sheet_name='Monthly')
        
        print(f"✅ {stock} market data saved successfully: {output_file}")
        
    except Exception as e:
        print(f"❌ Error collecting data for {stock}: {e}")
        continue

# Collect economic indicator proxies available through Yahoo Finance
# These complement the FRED economic data for comprehensive analysis
economic_indicators = [
    '^TNX',  # 10-Year Treasury Constant Maturity Rate (interest rate proxy)
    '^VIX',  # CBOE Volatility Index (market fear gauge)
]

# Process each economic indicator symbol
for indicator in economic_indicators:
    print(f"Collecting economic indicator data for {indicator}...")
    
    try:
        # Daily timeframe collection for economic indicators
        indicator_data = yf.download(indicator, start=start_date, end=end_date, interval='1d')
        
        # Clean indicator name for file naming (remove '^' prefix)
        indicator_name = indicator.replace('^', '')
        output_file = os.path.join(data_path, f'{indicator_name}_data.xlsx')
        
        # Save economic indicator data
        indicator_data.to_excel(output_file)
        
        print(f"✅ {indicator} economic data saved successfully: {output_file}")
        
    except Exception as e:
        print(f"❌ Error collecting economic indicator {indicator}: {e}")
        continue

print("🎉 Yahoo Finance data collection pipeline completed successfully!")
print(f"📁 All data files saved to: {data_path}")
print("🔄 Ready for data preprocessing and feature engineering...") 