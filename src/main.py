"""
QuantML: Machine Learning-Driven Quantitative Trading System
Main Execution Pipeline

This script orchestrates the complete data collection and processing pipeline
for the quantitative trading system including market data, economic indicators,
and news sentiment analysis.

Features:
- Multi-source data collection (Yahoo Finance, FRED, News APIs)
- Automated data preprocessing and feature engineering
- News sentiment analysis integration
- Comprehensive error handling and logging
"""

import os
import subprocess
import time
import sys
from datetime import datetime

def print_banner():
    """Print the system banner."""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║                        QuantML                            ║
    ║            Machine Learning-Driven Trading System         ║
    ║                                                           ║
    ║  🚀 Multi-Source Data Pipeline                            ║
    ║  📊 ML-Based Signal Generation                            ║
    ║  💹 Risk-Adjusted Portfolio Optimization                  ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)
    print(f"Pipeline started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)

def run_script(script_path, description, optional=False):
    """
    Execute a Python script with enhanced error handling.
    
    Args:
        script_path: Path to the script to execute
        description: Human-readable description of the script
        optional: Whether the script is optional (won't stop pipeline if fails)
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"\n{'='*80}")
    print(f"🔄 {description}")
    print(f"{'='*80}")
    
    try:
        start_time = time.time()
        result = subprocess.run(
            [sys.executable, script_path], 
            check=True,
            capture_output=True,
            text=True
        )
        
        execution_time = time.time() - start_time
        print(f"✅ {description} completed successfully!")
        print(f"⏱️  Execution time: {execution_time:.2f} seconds")
        
        # Print any relevant output
        if result.stdout:
            print(f"📄 Output preview:\n{result.stdout[:500]}...")
            
        return True
        
    except subprocess.CalledProcessError as e:
        execution_time = time.time() - start_time
        error_msg = f"❌ {description} failed after {execution_time:.2f} seconds"
        
        if optional:
            print(f"⚠️  {error_msg} (optional - continuing pipeline)")
            if e.stderr:
                print(f"🔍 Error details: {e.stderr[:300]}...")
            return True  # Continue pipeline for optional components
        else:
            print(error_msg)
            if e.stderr:
                print(f"🔍 Error details: {e.stderr[:500]}...")
            return False
    
    except Exception as e:
        print(f"💥 Unexpected error in {description}: {str(e)}")
        return False if not optional else True

def setup_environment():
    """Set up the necessary directories and environment."""
    print("\n🔧 Setting up environment...")
    
    # Create data directories
    directories = [
        'data/raw',
        'data/processed',
        'data/news',
        'logs',
        'models',
        'results'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  📁 Created/verified directory: {directory}")
    
    print("✅ Environment setup completed!")

def collect_api_keys():
    """Collect and validate API keys from user."""
    print("\n🔑 API Key Configuration")
    print("=" * 30)
    
    api_keys = {}
    
    # FRED API Key
    print("\n📊 FRED Economic Data API")
    print("Get your free API key from: https://fred.stlouisfed.org/docs/api/api_key.html")
    fred_key = input("Enter FRED API key (or press Enter to skip): ").strip()
    if fred_key:
        api_keys['FRED_API_KEY'] = fred_key
        os.environ['FRED_API_KEY'] = fred_key
    
    # News API Key
    print("\n📰 News Data API")
    print("Get your free API key from: https://newsapi.org/register")
    news_key = input("Enter NewsAPI key (or press Enter to skip): ").strip()
    if news_key:
        api_keys['NEWS_API_KEY'] = news_key
        os.environ['NEWS_API_KEY'] = news_key
    
    # Alpha Vantage API Key
    print("\n📈 Alpha Vantage API (for enhanced news sentiment)")
    print("Get your free API key from: https://www.alphavantage.co/support/#api-key")
    alpha_key = input("Enter Alpha Vantage API key (or press Enter to skip): ").strip()
    if alpha_key:
        api_keys['ALPHA_VANTAGE_KEY'] = alpha_key
        os.environ['ALPHA_VANTAGE_KEY'] = alpha_key
    
    return api_keys

def update_api_keys_in_scripts(api_keys):
    """Update API keys in the data collection scripts."""
    if 'FRED_API_KEY' in api_keys:
        # Update FRED script
        try:
            with open('src/data_collection/data_collection_fred.py', 'r') as file:
                content = file.read()
            
            # Replace the placeholder API key
            content = content.replace(
                "fred_api_key = '793c594fd13b09a517072cc115c1421e'", 
                f"fred_api_key = '{api_keys['FRED_API_KEY']}'"
            )
            
            with open('src/data_collection/data_collection_fred.py', 'w') as file:
                file.write(content)
                
            print("✅ Updated FRED API key in script")
        except Exception as e:
            print(f"⚠️  Warning: Could not update FRED API key: {e}")

def main():
    """
    Main execution pipeline for the QuantML trading system.
    """
    print_banner()
    
    # Setup environment
    setup_environment()
    
    # Collect API keys
    api_keys = collect_api_keys()
    update_api_keys_in_scripts(api_keys)
    
    print(f"\n🚀 Starting comprehensive data collection pipeline...")
    print(f"📅 Pipeline execution date: {datetime.now().strftime('%Y-%m-%d')}")
    
    pipeline_start_time = time.time()
    failed_steps = []
    
    # Step 1: Market Data Collection (Yahoo Finance)
    print(f"\n{'🏢 MARKET DATA COLLECTION':=^80}")
    if not run_script(
        'src/data_collection/data_collection_yahoo.py', 
        'Collecting market data from Yahoo Finance (NVDA, SOXL, XOM)'
    ):
        failed_steps.append("Market Data Collection")
        print("💥 Critical failure: Cannot proceed without market data")
        return False
    
    # Step 2: Economic Data Collection (FRED)
    print(f"\n{'📊 ECONOMIC DATA COLLECTION':=^80}")
    if 'FRED_API_KEY' in api_keys:
        if not run_script(
            'src/data_collection/data_collection_fred.py',
            'Collecting economic indicators from FRED API',
            optional=True
        ):
            failed_steps.append("Economic Data Collection")
    else:
        print("⚠️  Skipping FRED data collection - no API key provided")
    
    # Step 3: News & Sentiment Data Collection
    print(f"\n{'📰 NEWS & SENTIMENT ANALYSIS':=^80}")
    if 'NEWS_API_KEY' in api_keys or 'ALPHA_VANTAGE_KEY' in api_keys:
        if not run_script(
            'src/data_collection/data_collection_news.py',
            'Collecting news data and performing sentiment analysis',
            optional=True
        ):
            failed_steps.append("News Data Collection")
    else:
        print("⚠️  Skipping news data collection - no API keys provided")
        print("💡 Tip: Add NEWS_API_KEY or ALPHA_VANTAGE_KEY for enhanced signals")
    
    # Step 4: Data Preprocessing & Feature Engineering
    print(f"\n{'⚙️ DATA PROCESSING & FEATURE ENGINEERING':=^80}")
    if not run_script(
        'src/data_processing/data_preprocessing.py',
        'Processing and engineering features from collected data'
    ):
        failed_steps.append("Data Preprocessing")
        print("💥 Critical failure: Data preprocessing failed")
        return False
    
    # Pipeline Summary
    total_time = time.time() - pipeline_start_time
    print(f"\n{'📋 PIPELINE EXECUTION SUMMARY':=^80}")
    print(f"⏱️  Total execution time: {total_time:.2f} seconds ({total_time/60:.1f} minutes)")
    print(f"📊 API keys configured: {len(api_keys)}")
    
    if failed_steps:
        print(f"⚠️  Failed steps: {', '.join(failed_steps)}")
        print("💡 The pipeline completed with some optional components skipped")
    else:
        print("🎉 All pipeline steps completed successfully!")
    
    # Data Summary
    print(f"\n{'📁 DATA SUMMARY':=^80}")
    print("📊 Data files generated:")
    
    data_locations = {
        "Raw market data": "data/raw/*_data.xlsx",
        "Processed features": "data/processed/*_processed.csv", 
        "Economic indicators": "data/raw/economic_indicators.xlsx",
        "News sentiment": "data/raw/news_*.csv"
    }
    
    for desc, path in data_locations.items():
        print(f"  • {desc}: {path}")
    
    # Next Steps
    print(f"\n{'🚀 NEXT STEPS':=^80}")
    print("1. 📈 Review processed data in data/processed/ directory")
    print("2. 🔍 Analyze sentiment data for trading signals")
    print("3. 🤖 Run ML model training and optimization")
    print("4. 📊 Execute backtesting and performance validation")
    print("5. 💹 Deploy trading strategy with risk management")
    
    print(f"\n{'✅ QUANTML PIPELINE COMPLETED':=^80}")
    print(f"🎯 Ready for ML model training and strategy optimization!")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n🏆 Pipeline executed successfully! System ready for trading.")
            sys.exit(0)
        else:
            print("\n💥 Pipeline failed. Please check errors above.")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Pipeline interrupted by user. Exiting gracefully...")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error in main pipeline: {str(e)}")
        sys.exit(1) 