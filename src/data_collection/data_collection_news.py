"""
News Data Collection and Sentiment Analysis Pipeline

This script collects financial news data from multiple sources and performs
sentiment analysis for trading signal generation.

Features:
- NewsAPI integration for real-time financial news
- AlphaVantage news sentiment
- SEC EDGAR filing sentiment analysis
- Entity-specific news filtering
- Temporal sentiment aggregation
- News impact decay modeling
"""

import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
from textblob import TextBlob
import json
import time
from typing import Dict, List, Optional
import warnings
warnings.filterwarnings('ignore')

# Project root and data paths
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
data_path = os.path.join(project_root, 'data', 'raw')
os.makedirs(data_path, exist_ok=True)

class NewsDataCollector:
    """
    Comprehensive news data collection and sentiment analysis for financial trading.
    """
    
    def __init__(self, newsapi_key: Optional[str] = None, alphavantage_key: Optional[str] = None):
        """
        Initialize the news data collector.
        
        Args:
            newsapi_key: NewsAPI.org API key
            alphavantage_key: Alpha Vantage API key
        """
        self.newsapi_key = newsapi_key or os.getenv('NEWS_API_KEY')
        self.alphavantage_key = alphavantage_key or os.getenv('ALPHA_VANTAGE_KEY')
        
        # Target symbols for news collection
        self.symbols = ['NVDA', 'SOXL', 'XOM', 'AAPL', 'MSFT', 'GOOGL', 'TSLA']
        
        # News sources configuration
        self.financial_sources = [
            'bloomberg', 'reuters', 'cnbc', 'marketwatch', 'yahoo-finance',
            'financial-times', 'the-wall-street-journal', 'business-insider',
            'fortune', 'forbes'
        ]
        
        print("📰 News Data Collector initialized")
        if not self.newsapi_key:
            print("⚠️  Warning: No NewsAPI key provided. Some features will be limited.")
    
    def get_company_info(self, symbol: str) -> Dict:
        """Get company information for better news filtering."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            return {
                'symbol': symbol,
                'company_name': info.get('longName', symbol),
                'sector': info.get('sector', ''),
                'industry': info.get('industry', ''),
                'keywords': [
                    symbol,
                    info.get('longName', '').replace(' Inc.', '').replace(' Corp.', ''),
                    info.get('shortName', '')
                ]
            }
        except Exception as e:
            print(f"Warning: Could not fetch info for {symbol}: {e}")
            return {'symbol': symbol, 'company_name': symbol, 'keywords': [symbol]}
    
    def collect_newsapi_data(self, symbol: str, days_back: int = 30) -> List[Dict]:
        """
        Collect news data from NewsAPI.
        
        Args:
            symbol: Stock symbol
            days_back: Number of days to look back
            
        Returns:
            List of news articles with metadata
        """
        if not self.newsapi_key:
            print(f"⚠️  Skipping NewsAPI collection for {symbol} - no API key")
            return []
        
        company_info = self.get_company_info(symbol)
        articles = []
        
        # Build search query
        keywords = company_info['keywords']
        query = f'({" OR ".join(keywords)}) AND (stock OR trading OR earnings OR financial)'
        
        # Date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        url = 'https://newsapi.org/v2/everything'
        params = {
            'q': query,
            'sources': ','.join(self.financial_sources),
            'from': start_date.strftime('%Y-%m-%d'),
            'to': end_date.strftime('%Y-%m-%d'),
            'sortBy': 'publishedAt',
            'language': 'en',
            'apiKey': self.newsapi_key,
            'pageSize': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'ok':
                for article in data['articles']:
                    if self._is_relevant_article(article, symbol, company_info):
                        articles.append({
                            'symbol': symbol,
                            'title': article['title'],
                            'description': article['description'],
                            'content': article['content'],
                            'source': article['source']['name'],
                            'url': article['url'],
                            'published_at': article['publishedAt'],
                            'collected_at': datetime.now().isoformat()
                        })
            
            print(f"✅ Collected {len(articles)} relevant articles for {symbol} from NewsAPI")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error collecting NewsAPI data for {symbol}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {symbol}: {e}")
        
        return articles
    
    def collect_alphavantage_sentiment(self, symbol: str) -> List[Dict]:
        """
        Collect news sentiment from Alpha Vantage.
        
        Args:
            symbol: Stock symbol
            
        Returns:
            List of news articles with sentiment scores
        """
        if not self.alphavantage_key:
            print(f"⚠️  Skipping Alpha Vantage collection for {symbol} - no API key")
            return []
        
        articles = []
        url = 'https://www.alphavantage.co/query'
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': symbol,
            'apikey': self.alphavantage_key,
            'limit': 200
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if 'feed' in data:
                for item in data['feed']:
                    # Extract ticker-specific sentiment if available
                    ticker_sentiment = None
                    if 'ticker_sentiment' in item:
                        for ts in item['ticker_sentiment']:
                            if ts['ticker'] == symbol:
                                ticker_sentiment = ts
                                break
                    
                    articles.append({
                        'symbol': symbol,
                        'title': item['title'],
                        'summary': item['summary'],
                        'source': item['source'],
                        'url': item['url'],
                        'published_at': item['time_published'],
                        'overall_sentiment_score': float(item['overall_sentiment_score']),
                        'overall_sentiment_label': item['overall_sentiment_label'],
                        'ticker_sentiment_score': float(ticker_sentiment['relevance_score']) if ticker_sentiment else 0.0,
                        'ticker_sentiment_label': ticker_sentiment['ticker_sentiment_label'] if ticker_sentiment else 'Neutral',
                        'collected_at': datetime.now().isoformat()
                    })
            
            print(f"✅ Collected {len(articles)} sentiment articles for {symbol} from Alpha Vantage")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error collecting Alpha Vantage data for {symbol}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error for {symbol}: {e}")
        
        return articles
    
    def _is_relevant_article(self, article: Dict, symbol: str, company_info: Dict) -> bool:
        """
        Check if an article is relevant to the target symbol.
        
        Args:
            article: Article data from NewsAPI
            symbol: Target stock symbol
            company_info: Company information
            
        Returns:
            Boolean indicating relevance
        """
        # Combine title and description for analysis
        text = f"{article.get('title', '')} {article.get('description', '')}".lower()
        
        # Check for symbol and company name mentions
        keywords = [kw.lower() for kw in company_info['keywords'] if kw]
        
        # Must mention at least one keyword
        if not any(keyword in text for keyword in keywords):
            return False
        
        # Filter out irrelevant articles
        irrelevant_keywords = ['obituary', 'weather', 'sports', 'entertainment', 'celebrity']
        if any(keyword in text for keyword in irrelevant_keywords):
            return False
        
        return True
    
    def calculate_sentiment_score(self, text: str) -> float:
        """
        Calculate sentiment score using TextBlob.
        
        Args:
            text: Text to analyze
            
        Returns:
            Sentiment score between -1 and 1
        """
        if not text:
            return 0.0
        
        try:
            blob = TextBlob(text)
            # TextBlob polarity is between -1 and 1
            return blob.sentiment.polarity
        except Exception:
            return 0.0
    
    def aggregate_daily_sentiment(self, articles: List[Dict]) -> pd.DataFrame:
        """
        Aggregate news sentiment by day.
        
        Args:
            articles: List of articles with sentiment
            
        Returns:
            DataFrame with daily sentiment aggregations
        """
        if not articles:
            return pd.DataFrame()
        
        df = pd.DataFrame(articles)
        
        # Parse publication dates
        if 'published_at' in df.columns:
            df['date'] = pd.to_datetime(df['published_at']).dt.date
        elif 'time_published' in df.columns:
            df['date'] = pd.to_datetime(df['time_published'], format='%Y%m%dT%H%M%S').dt.date
        
        # Calculate sentiment if not provided
        if 'sentiment_score' not in df.columns:
            if 'overall_sentiment_score' in df.columns:
                df['sentiment_score'] = df['overall_sentiment_score']
            else:
                df['sentiment_score'] = df.apply(
                    lambda row: self.calculate_sentiment_score(
                        f"{row.get('title', '')} {row.get('description', '')} {row.get('summary', '')}"
                    ), axis=1
                )
        
        # Aggregate by date and symbol
        daily_sentiment = df.groupby(['symbol', 'date']).agg({
            'sentiment_score': ['mean', 'std', 'count'],
            'url': 'count'  # Article count
        }).round(4)
        
        # Flatten column names
        daily_sentiment.columns = ['sentiment_mean', 'sentiment_std', 'sentiment_count', 'article_count']
        daily_sentiment.reset_index(inplace=True)
        
        # Calculate confidence score based on article count and sentiment consistency
        daily_sentiment['sentiment_confidence'] = np.minimum(
            daily_sentiment['article_count'] / 10,  # More articles = higher confidence
            1.0
        ) * (1 - daily_sentiment['sentiment_std'].fillna(0.5))  # Lower std = higher confidence
        
        return daily_sentiment
    
    def collect_all_news_data(self, days_back: int = 30) -> Dict[str, pd.DataFrame]:
        """
        Collect news data from all sources for all symbols.
        
        Args:
            days_back: Number of days to look back
            
        Returns:
            Dictionary with DataFrames for each data source
        """
        all_newsapi_articles = []
        all_alphavantage_articles = []
        
        print(f"🚀 Starting news collection for {len(self.symbols)} symbols...")
        
        for i, symbol in enumerate(self.symbols, 1):
            print(f"\n📊 Processing {symbol} ({i}/{len(self.symbols)})...")
            
            # Collect from NewsAPI
            newsapi_articles = self.collect_newsapi_data(symbol, days_back)
            all_newsapi_articles.extend(newsapi_articles)
            
            # Collect from Alpha Vantage
            alphavantage_articles = self.collect_alphavantage_sentiment(symbol)
            all_alphavantage_articles.extend(alphavantage_articles)
            
            # Rate limiting
            if i < len(self.symbols):
                time.sleep(1)  # Avoid hitting API rate limits
        
        # Create aggregated sentiment DataFrames
        results = {}
        
        if all_newsapi_articles:
            newsapi_sentiment = self.aggregate_daily_sentiment(all_newsapi_articles)
            results['newsapi_sentiment'] = newsapi_sentiment
            results['newsapi_raw'] = pd.DataFrame(all_newsapi_articles)
        
        if all_alphavantage_articles:
            alphavantage_sentiment = self.aggregate_daily_sentiment(all_alphavantage_articles)
            results['alphavantage_sentiment'] = alphavantage_sentiment
            results['alphavantage_raw'] = pd.DataFrame(all_alphavantage_articles)
        
        return results
    
    def save_news_data(self, data: Dict[str, pd.DataFrame], output_dir: str = None) -> None:
        """
        Save collected news data to files.
        
        Args:
            data: Dictionary of DataFrames to save
            output_dir: Output directory (defaults to data/raw)
        """
        if output_dir is None:
            output_dir = data_path
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for data_type, df in data.items():
            if not df.empty:
                filename = f"news_{data_type}_{timestamp}.csv"
                filepath = os.path.join(output_dir, filename)
                df.to_csv(filepath, index=False)
                print(f"💾 Saved {data_type}: {filepath} ({len(df)} rows)")


def main():
    """
    Main execution function for news data collection.
    """
    print("🎯 Financial News Data Collection Pipeline")
    print("=" * 50)
    
    # Initialize collector
    collector = NewsDataCollector()
    
    # Collect news data
    print("\n📈 Collecting financial news data...")
    news_data = collector.collect_all_news_data(days_back=30)
    
    if news_data:
        # Save data
        print("\n💾 Saving collected data...")
        collector.save_news_data(news_data)
        
        # Print summary
        print("\n📊 Collection Summary:")
        for data_type, df in news_data.items():
            print(f"  • {data_type}: {len(df)} records")
    else:
        print("\n⚠️  No news data collected. Please check API keys and internet connection.")
    
    print("\n✅ News collection pipeline completed!")


if __name__ == "__main__":
    main() 