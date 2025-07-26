"""
Data Processing Module for QuantML Trading System

This package provides advanced data preprocessing and feature engineering capabilities
for the machine learning-driven quantitative trading system.

Key Features:
- Statistical outlier detection using Z-score methodology
- Multi-timeframe price normalization and scaling
- Technical indicator calculation (moving averages, volatility measures)
- Missing value imputation using forward-fill and backward-fill
- Feature engineering for ML model input preparation
- Risk metric calculation (ATR, volatility scores, outlier scores)

Processing Pipeline:
1. Raw data validation and cleaning
2. Outlier detection and scoring (non-removal approach)
3. Technical indicator calculation across multiple timeframes
4. Price movement normalization (0-1 scaling)
5. Risk metric computation for position sizing
6. Feature aggregation for ML model consumption

Modules:
- data_preprocessing: Core preprocessing functionality with statistical methods

Usage:
    from src.data_processing import *
    
    # Direct function imports available:
    # from src.data_processing.data_preprocessing import normalize_price_movements
    # from src.data_processing.data_preprocessing import detect_outliers
"""

from .data_preprocessing import * 