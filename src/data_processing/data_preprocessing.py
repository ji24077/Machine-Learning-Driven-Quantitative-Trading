"""
Data Preprocessing Module for QuantML Trading System

This module provides comprehensive data preprocessing and feature engineering capabilities
for the machine learning-driven quantitative trading system.

Key Features:
- Z-score based outlier detection (non-removal approach for ML training)
- Multi-timeframe price movement normalization (0-1 scaling)
- Technical indicator calculation (moving averages, volatility measures)
- Risk metric computation (ATR proxy, outlier scores)
- Missing value imputation using forward-fill and backward-fill methods
- Automated processing pipeline for both market and economic data

Processing Pipeline:
1. Raw data validation and type conversion
2. Outlier detection and scoring (preserves extreme values as features)
3. Price normalization and return calculation
4. Technical indicator generation (MA_5, MA_20, MA_50)
5. Volatility and risk metric calculation
6. Missing value imputation for time series continuity

Output:
- Processed CSV files ready for ML model consumption
- Enhanced feature sets with technical and risk indicators
- Normalized economic indicators for macroeconomic signal generation
"""

import pandas as pd
import numpy as np
import os
# from scipy import stats  # Using NumPy instead of SciPy for reduced dependencies
import glob

# Configure data directory paths for input and output
raw_data_dir = 'data/raw'
processed_data_dir = 'data/processed'

# Create directory for processed data storage
os.makedirs(processed_data_dir, exist_ok=True)

def detect_outliers(series, threshold=3):
    """
    Detect outliers using Z-score methodology with NumPy implementation.
    
    This function identifies extreme values in time series data without removing them,
    preserving all data points for ML model training while marking unusual observations.
    
    Args:
        series (pd.Series): Input data series for outlier detection
        threshold (float): Z-score threshold for outlier classification (default: 3)
    
    Returns:
        np.ndarray: Boolean mask indicating outlier positions (True = outlier)
        
    Note:
        Uses robust Z-score calculation: |x - μ| / σ > threshold
        Handles missing values by dropping NaN before calculation
    """
    series_no_nan = series.dropna()
    mean = np.mean(series_no_nan)
    std = np.std(series_no_nan)
    z_scores = np.abs((series_no_nan - mean) / std) if std > 0 else np.zeros_like(series_no_nan)
    return z_scores > threshold

def calculate_outlier_score(series):
    """
    Calculate normalized outlier scores using Z-score methodology.
    
    Converts Z-scores to a 0-1 scale for use as ML features, providing
    continuous outlier intensity rather than binary classification.
    
    Args:
        series (pd.Series): Input data series for outlier scoring
    
    Returns:
        pd.Series: Normalized outlier scores (0-1 range) with original index
        
    Note:
        - 0 indicates normal behavior, 1 indicates extreme outlier
        - Preserves temporal index for time series alignment
        - Handles edge cases (zero variance) gracefully
    """
    series_no_nan = series.dropna()
    mean = np.mean(series_no_nan)
    std = np.std(series_no_nan)
    
    if std > 0:
        z_scores = np.abs((series_no_nan - mean) / std)
        # Normalize Z-scores to 0-1 range for feature scaling
        min_z = np.min(z_scores)
        max_z = np.max(z_scores)
        outlier_scores = (z_scores - min_z) / (max_z - min_z) if max_z > min_z else z_scores
    else:
        outlier_scores = np.zeros_like(series_no_nan)
    
    return pd.Series(outlier_scores, index=series_no_nan.index)

def normalize_price_movements(df):
    """
    Comprehensive price movement normalization and feature engineering.
    
    Transforms raw OHLCV data into normalized features suitable for ML model training,
    including technical indicators, risk metrics, and outlier scores.
    
    Args:
        df (pd.DataFrame): Raw market data with OHLCV columns
    
    Returns:
        pd.DataFrame: Enhanced dataset with engineered features:
            - Returns: Period-over-period price changes
            - NormalizedPrice: Min-max scaled prices (0-1)
            - MA_5, MA_20, MA_50: Moving averages for trend analysis
            - Volatility: High-Low range (ATR proxy)
            - ReturnsOutlierScore: Outlier intensity for returns
            - VolatilityOutlierScore: Outlier intensity for volatility
            
    Note:
        - Preserves all original data while adding features
        - Handles missing values with forward-fill then backward-fill
        - Validates data types and converts strings to numeric when needed
    """
    # Define expected numeric columns for validation and conversion
    numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    for col in numeric_columns:
        if col in df.columns:
            # Convert string data to numeric (remove commas and cast to float)
            if df[col].dtype == 'object':
                try:
                    df[col] = df[col].replace({',': ''}, regex=True).astype(float)
                except Exception as e:
                    print(f"  ⚠️  Warning: Cannot convert {col} column to numeric. Error: {e}")
    
    # Calculate price returns for momentum signal generation
    if 'Close' in df.columns and df['Close'].dtype != 'object':
        df['Returns'] = df['Close'].pct_change(fill_method=None)
        
        # Min-max normalization for price levels (0-1 scaling)
        min_price = df['Close'].min()
        max_price = df['Close'].max()
        if max_price > min_price:
            df['NormalizedPrice'] = (df['Close'] - min_price) / (max_price - min_price)
        
        # Calculate moving averages for trend identification
        df['MA_5'] = df['Close'].rolling(window=5).mean()      # Short-term trend
        df['MA_20'] = df['Close'].rolling(window=20).mean()    # Medium-term trend  
        df['MA_50'] = df['Close'].rolling(window=50).mean()    # Long-term trend
        
        # Calculate volatility proxy using High-Low range (simplified ATR)
        if 'High' in df.columns and 'Low' in df.columns:
            df['Volatility'] = df['High'] - df['Low']
            
            # Generate outlier scores for risk management features
            if 'Returns' in df.columns:
                returns_outlier_score = calculate_outlier_score(df['Returns'])
                df.loc[returns_outlier_score.index, 'ReturnsOutlierScore'] = returns_outlier_score
            
            if 'Volatility' in df.columns:
                volatility_outlier_score = calculate_outlier_score(df['Volatility'])
                df.loc[volatility_outlier_score.index, 'VolatilityOutlierScore'] = volatility_outlier_score
    else:
        print("  ⚠️  Warning: 'Close' column missing or non-numeric. Some indicators cannot be calculated.")
    
    # Handle missing values using time series appropriate methods
    df.fillna(method='ffill', inplace=True)  # Forward fill for time series continuity
    df.fillna(method='bfill', inplace=True)  # Backward fill for remaining gaps
    
    return df

# Process market data files (stocks and ETFs)
print("🚀 Starting market data preprocessing pipeline...")
stock_files = glob.glob(f"{raw_data_dir}/*_data.xlsx")

for file_path in stock_files:
    stock_name = os.path.basename(file_path).split('_')[0]
    print(f"📊 Processing market data for {stock_name}...")
    
    try:
        # Read Excel file with multiple timeframe sheets
        with pd.ExcelFile(file_path) as xls:
            # Process each timeframe (Daily, Weekly, Monthly)
            for sheet_name in xls.sheet_names:
                print(f"  🔄 Processing {sheet_name} timeframe...")
                df = pd.read_excel(xls, sheet_name=sheet_name)
                
                # Display data structure for validation
                print(f"    📋 Columns: {df.columns.tolist()}")
                print(f"    🔍 Data types: {df.dtypes.tolist()}")
                
                # Ensure proper datetime index for time series operations
                if not isinstance(df.index, pd.DatetimeIndex) and 'Date' in df.columns:
                    df.set_index('Date', inplace=True)
                
                # Apply comprehensive preprocessing pipeline
                processed_df = normalize_price_movements(df)
                
                # Save processed data with descriptive naming convention
                output_file = f"{processed_data_dir}/{stock_name}_{sheet_name.lower()}_processed.csv"
                processed_df.to_csv(output_file)
                print(f"    ✅ {sheet_name} data processing completed: {output_file}")
                
    except Exception as e:
        print(f"    ❌ Error: Failed to process {stock_name} data: {e}")
        continue

# Process economic indicators data for macroeconomic signals
print("\n📈 Processing economic indicators data...")
economic_file = f"{raw_data_dir}/economic_indicators.xlsx"

if os.path.exists(economic_file):
    print("🔄 Preprocessing economic indicators dataset...")
    
    try:
        # Read economic indicators with date index
        economic_df = pd.read_excel(economic_file, index_col=0)
        
        # Handle missing values in economic time series
        economic_df.fillna(method='ffill', inplace=True)
        
        # Normalize each economic indicator for ML model consumption
        for column in economic_df.columns:
            # Convert string data to numeric format
            if economic_df[column].dtype == 'object':
                try:
                    economic_df[column] = economic_df[column].replace({',': ''}, regex=True).astype(float)
                except:
                    print(f"    ⚠️  Warning: Cannot convert {column} column to numeric format")
                    continue
            
            # Apply min-max normalization to economic indicators
            min_val = economic_df[column].min()
            max_val = economic_df[column].max()
            if max_val > min_val:
                economic_df[f"{column}_Normalized"] = (economic_df[column] - min_val) / (max_val - min_val)
        
        # Save processed economic indicators
        output_file = f"{processed_data_dir}/economic_indicators_processed.csv"
        economic_df.to_csv(output_file)
        print(f"✅ Economic indicators processing completed: {output_file}")
        print(f"📊 Processed {len(economic_df.columns)} economic indicators")
        
    except Exception as e:
        print(f"❌ Error: Economic indicators processing failed: {e}")
else:
    print("⚠️  Economic indicators file not found - skipping economic data processing")

print("\n🎉 Data preprocessing pipeline completed successfully!")
print(f"📁 Processed files saved to: {os.path.abspath(processed_data_dir)}")
print("🤖 Ready for ML model training and feature engineering...") 