"""
Federal Reserve Economic Data (FRED) Collection Module

This module collects macroeconomic indicators from the Federal Reserve Economic Data (FRED) API
for the QuantML trading system. These indicators provide crucial economic context for trading decisions.

Features:
- Real-time economic indicator retrieval from FRED API
- Comprehensive macroeconomic data coverage (GDP, CPI, employment, etc.)
- Automated data validation and error handling
- Excel format output for downstream processing
- 10-year historical data collection for sufficient ML training

Economic Indicators Collected:
- GDP: Real Gross Domestic Product (economic growth)
- CPI: Consumer Price Index (inflation measure)  
- UNRATE: Unemployment Rate (labor market health)
- FEDFUNDS: Federal Funds Rate (monetary policy indicator)
- PAYEMS: Total Nonfarm Payrolls (employment level)
- INDPRO: Industrial Production Index (manufacturing activity)

API Requirements:
- FRED API key (free registration at https://fred.stlouisfed.org/docs/api/api_key.html)
- Internet connection for real-time data retrieval
"""

import pandas as pd
import os
from fredapi import Fred
from datetime import datetime, timedelta

# Create directory for raw economic data storage
os.makedirs('data/raw', exist_ok=True)

# FRED API key configuration
# Note: Replace with your personal API key from FRED registration
fred_api_key = '793c594fd13b09a517072cc115c1421e'  # API key configured

# Initialize FRED API connection with error handling
try:
    fred = Fred(api_key=fred_api_key)
    print("✅ FRED API connection established successfully")
except Exception as e:
    print(f"❌ FRED API connection failed: {e}")
    print("💡 Please obtain your API key from FRED and update the script")
    exit(1)

# Define economic indicators for comprehensive macroeconomic analysis
# Each indicator provides unique insights into different economic aspects
economic_indicators = {
    'GDP': 'GDP',                      # Real GDP - overall economic output
    'CPIAUCSL': 'CPI',                # Consumer Price Index - inflation measure
    'UNRATE': 'Unemployment',          # Unemployment Rate - labor market condition
    'FEDFUNDS': 'FedRate',            # Federal Funds Rate - monetary policy tool
    'PAYEMS': 'Employment',           # Nonfarm Payrolls - employment level
    'INDPRO': 'IndustrialProduction', # Industrial Production - manufacturing activity
}

# Configure data collection timeframe (10 years for ML model training)
end_date = datetime.now()
start_date = end_date - timedelta(days=365*10)

# Initialize DataFrame to store all economic indicators
all_economic_data = pd.DataFrame()

# Collect each economic indicator with individual error handling
for series_id, indicator_name in economic_indicators.items():
    print(f"📊 Collecting {indicator_name} data (Series: {series_id})...")
    
    try:
        # Retrieve economic data from FRED API
        data = fred.get_series(series_id, start_date, end_date)
        
        # Assign descriptive column name for clarity
        data.name = indicator_name
        
        # Aggregate all indicators into comprehensive dataset
        if all_economic_data.empty:
            all_economic_data = pd.DataFrame(data)
        else:
            all_economic_data = pd.concat([all_economic_data, pd.DataFrame(data)], axis=1)
        
        print(f"✅ {indicator_name} data collected successfully ({len(data)} observations)")
        
    except Exception as e:
        print(f"❌ Failed to collect {indicator_name} data: {e}")
        print(f"   Series ID: {series_id} may be unavailable or require different access")
        continue

# Save comprehensive economic dataset if any data was collected
if not all_economic_data.empty:
    output_file = 'data/raw/economic_indicators.xlsx'
    all_economic_data.to_excel(output_file)
    print(f"🎉 Economic indicators dataset saved successfully: {output_file}")
    print(f"📊 Dataset contains {len(all_economic_data.columns)} indicators across {len(all_economic_data)} time periods")
    
    # Display dataset summary for verification
    print("\n📋 Economic Dataset Summary:")
    for col in all_economic_data.columns:
        non_null_count = all_economic_data[col].count()
        date_range = f"{all_economic_data[col].first_valid_index()} to {all_economic_data[col].last_valid_index()}"
        print(f"   • {col}: {non_null_count} observations ({date_range})")
        
else:
    print("⚠️  No economic indicator data was collected successfully")
    print("💡 Please check your FRED API key and internet connection")

print("🔄 FRED economic data collection pipeline completed!")
print("📈 Ready for integration with market data and preprocessing...") 