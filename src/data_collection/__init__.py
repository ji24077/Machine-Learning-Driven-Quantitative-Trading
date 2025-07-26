"""
Data Collection Module for QuantML Trading System

This package provides comprehensive data collection capabilities from multiple financial sources
for the machine learning-driven quantitative trading system.

Key Features:
- Yahoo Finance API integration for market data (OHLCV, technical indicators)
- FRED API integration for macroeconomic indicators (GDP, CPI, unemployment, etc.)
- News sentiment data collection from NewsAPI and Alpha Vantage
- Real-time and historical data retrieval with error handling
- Multi-timeframe data aggregation (daily, weekly, monthly)

Modules:
- data_collection_yahoo: Market data from Yahoo Finance API
- data_collection_fred: Economic indicators from Federal Reserve Economic Data
- data_collection_news: Financial news sentiment analysis from multiple sources

Usage:
    from src.data_collection import *
    
    # Individual module imports available:
    # from src.data_collection.data_collection_yahoo import collect_market_data
    # from src.data_collection.data_collection_fred import collect_economic_data
    # from src.data_collection.data_collection_news import NewsDataCollector
"""

from .data_collection_yahoo import *
from .data_collection_fred import * 