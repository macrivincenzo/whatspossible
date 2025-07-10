"""
Market analysis module for KDP research
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import logging
from collections import defaultdict
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketAnalyzer:
    def __init__(self):
        self.market_data = {}
        self.trends = {}
    
    def analyze_market_trends(self, books_data):
        """Analyze overall market trends"""
        logger.info("Analyzing market trends")
        
        df = pd.DataFrame(books_data)
        
        # Basic statistics
        stats = {
            'total_books': len(df),
            'avg_price': df['price'].mean() if 'price' in df.columns else 0,
            'avg_rating': df['rating'].mean() if 'rating' in df.columns else 0,
            'avg_reviews': df['review_count'].mean() if 'review_count' in df.columns else 0,
            'price_range': {
                'min': df['price'].min() if 'price' in df.columns else 0,
                'max': df['price'].max() if 'price' in df.columns else 0,
                'median': df['price'].median() if 'price' in df.columns else 0
            }
        }
        
        # Category analysis
        if 'category' in df.columns:
            category_stats = df.groupby('category').agg({
                'price': ['mean', 'median', 'count'],
                'rating': 'mean',
                'review_count': 'mean'
            }).round(2)
            stats['category_analysis'] = category_stats.to_dict()
        
        return stats
    
    def analyze_pricing_strategies(self, books_data):
        """Analyze pricing patterns and strategies"""
        logger.info("Analyzing pricing strategies")
        
        df = pd.DataFrame(books_data)
        
        if 'price' not in df.columns or df['price'].isna().all():
            return {'error': 'No pricing data available'}
        
        # Remove books with no price data
        df = df[df['price'] > 0]
        
        pricing_analysis = {
            'price_distribution': {
                'under_3': len(df[df['price'] < 3]),
                '3_to_5': len(df[(df['price'] >= 3) & (df['price'] < 5)]),
                '5_to_10': len(df[(df['price'] >= 5) & (df['price'] < 10)]),
                '10_to_15': len(df[(df['price'] >= 10) & (df['price'] < 15)]),
                'over_15': len(df[df['price'] >= 15])
            },
            'sweet_spot_analysis': self.find_pricing_sweet_spots(df),
            'price_vs_rating_correlation': self.analyze_price_rating_correlation(df),
            'optimal_price_ranges': self.calculate_optimal_prices(df)
        }
        
        return pricing_analysis
    
    def find_pricing_sweet_spots(self, df):
        """Find price ranges with best rating-to-competition ratio"""
        price_bins = [(0, 2.99), (3, 4.99), (5, 7.99), (8, 12.99), (13, 20), (20, float('inf'))]
        sweet_spots = []
        
        for min_price, max_price in price_bins:
            if max_price == float('inf'):
                subset = df[df['price'] >= min_price]
                range_name = f"${min_price}+"
            else:
                subset = df[(df['price'] >= min_price) & (df['price'] <= max_price)]
                range_name = f"${min_price}-${max_price}"
            
            if len(subset) > 0:
                avg_rating = subset['rating'].mean()
                book_count = len(subset)
                avg_reviews = subset['review_count'].mean()
                
                # Calculate competitiveness score (lower is better for new authors)
                competitiveness = book_count / len(df) * 100
                
                sweet_spots.append({
                    'price_range': range_name,
                    'avg_rating': round(avg_rating, 2),
                    'book_count': book_count,
                    'avg_reviews': int(avg_reviews),
                    'competitiveness': round(competitiveness, 1),
                    'opportunity_score': self.calculate_opportunity_score(avg_rating, book_count, avg_reviews)
                })
        
        return sorted(sweet_spots, key=lambda x: x['opportunity_score'], reverse=True)
    
    def calculate_opportunity_score(self, avg_rating, book_count, avg_reviews):
        """Calculate opportunity score for a price range"""
        # Higher rating is good, but too many books means high competition
        # Moderate review count is ideal
        
        score = 0
        
        # Rating factor (higher is better)
        if avg_rating >= 4.0:
            score += 30
        elif avg_rating >= 3.5:
            score += 20
        else:
            score += 10
        
        # Competition factor (fewer books is better for new authors)
        if book_count < 20:
            score += 40
        elif book_count < 50:
            score += 25
        elif book_count < 100:
            score += 10
        
        # Review factor (moderate is good)
        if 50 <= avg_reviews <= 200:
            score += 30
        elif 10 <= avg_reviews <= 500:
            score += 20
        elif avg_reviews > 0:
            score += 10
        
        return score
    
    def analyze_price_rating_correlation(self, df):
        """Analyze correlation between price and rating"""
        if len(df) < 10:
            return {'correlation': 0, 'insight': 'Insufficient data'}
        
        correlation = df['price'].corr(df['rating'])
        
        insights = []
        if correlation > 0.3:
            insights.append("Higher priced books tend to have better ratings")
        elif correlation < -0.3:
            insights.append("Lower priced books tend to have better ratings")
        else:
            insights.append("No strong correlation between price and rating")
        
        # Price vs review count correlation
        review_correlation = df['price'].corr(df['review_count'])
        if review_correlation > 0.3:
            insights.append("Higher priced books tend to have more reviews")
        elif review_correlation < -0.3:
            insights.append("Lower priced books tend to have more reviews")
        
        return {
            'price_rating_correlation': round(correlation, 3),
            'price_review_correlation': round(review_correlation, 3),
            'insights': insights
        }
    
    def calculate_optimal_prices(self, df):
        """Calculate optimal pricing based on market data"""
        # Group by rating ranges to find optimal prices
        rating_groups = [
            (4.5, 5.0, "Excellent"),
            (4.0, 4.5, "Very Good"),
            (3.5, 4.0, "Good"),
            (0, 3.5, "Average")
        ]
        
        optimal_prices = []
        
        for min_rating, max_rating, category in rating_groups:
            subset = df[(df['rating'] >= min_rating) & (df['rating'] < max_rating)]
            
            if len(subset) > 5:  # Need sufficient data
                median_price = subset['price'].median()
                q75_price = subset['price'].quantile(0.75)
                q25_price = subset['price'].quantile(0.25)
                
                optimal_prices.append({
                    'rating_category': category,
                    'suggested_price_range': f"${q25_price:.2f} - ${q75_price:.2f}",
                    'median_price': f"${median_price:.2f}",
                    'book_count': len(subset)
                })
        
        return optimal_prices
    
    def analyze_competition_gaps(self, books_data, keywords):
        """Identify market gaps and opportunities"""
        logger.info("Analyzing competition gaps")
        
        df = pd.DataFrame(books_data)
        gaps = []
        
        for keyword in keywords[:10]:  # Analyze top 10 keywords
            keyword_books = df[df['title'].str.contains(keyword, case=False, na=False)]
            
            if len(keyword_books) == 0:
                gaps.append({
                    'keyword': keyword,
                    'opportunity_type': 'No Competition',
                    'books_found': 0,
                    'recommendation': f"High opportunity - no books found for '{keyword}'"
                })
            elif len(keyword_books) < 10:
                gaps.append({
                    'keyword': keyword,
                    'opportunity_type': 'Low Competition',
                    'books_found': len(keyword_books),
                    'avg_rating': keyword_books['rating'].mean(),
                    'recommendation': f"Good opportunity - low competition for '{keyword}'"
                })
        
        return gaps
    
    def generate_market_insights(self, books_data):
        """Generate actionable market insights"""
        logger.info("Generating market insights")
        
        df = pd.DataFrame(books_data)
        insights = []
        
        # Pricing insights
        if 'price' in df.columns:
            avg_price = df['price'].mean()
            if avg_price < 5:
                insights.append("Market dominated by low-priced books - consider premium positioning")
            elif avg_price > 15:
                insights.append("High-priced market - opportunity for budget-friendly alternatives")
        
        # Rating insights
        if 'rating' in df.columns:
            avg_rating = df['rating'].mean()
            low_rated_books = len(df[df['rating'] < 3.5])
            if low_rated_books / len(df) > 0.3:
                insights.append("Many low-rated books - opportunity for quality content")
        
        # Review insights
        if 'review_count' in df.columns:
            low_review_books = len(df[df['review_count'] < 10])
            if low_review_books / len(df) > 0.5:
                insights.append("Many books with few reviews - marketing opportunity exists")
        
        # Category insights
        if 'category' in df.columns:
            category_counts = df['category'].value_counts()
            underserved = category_counts[category_counts < 10]
            if len(underserved) > 0:
                insights.append(f"Underserved categories: {', '.join(underserved.index[:3])}")
        
        return insights
    
    def create_market_visualization(self, books_data, output_path):
        """Create market analysis visualizations"""
        try:
            df = pd.DataFrame(books_data)
            
            fig, axes = plt.subplots(2, 2, figsize=(15, 10))
            fig.suptitle('KDP Market Analysis Dashboard', fontsize=16)
            
            # Price distribution
            if 'price' in df.columns and not df['price'].isna().all():
                axes[0, 0].hist(df['price'], bins=20, edgecolor='black', alpha=0.7)
                axes[0, 0].set_title('Price Distribution')
                axes[0, 0].set_xlabel('Price ($)')
                axes[0, 0].set_ylabel('Number of Books')
            
            # Rating distribution
            if 'rating' in df.columns and not df['rating'].isna().all():
                axes[0, 1].hist(df['rating'], bins=10, edgecolor='black', alpha=0.7, color='orange')
                axes[0, 1].set_title('Rating Distribution')
                axes[0, 1].set_xlabel('Rating')
                axes[0, 1].set_ylabel('Number of Books')
            
            # Price vs Rating scatter
            if 'price' in df.columns and 'rating' in df.columns:
                valid_data = df[(df['price'] > 0) & (df['rating'] > 0)]
                if len(valid_data) > 0:
                    axes[1, 0].scatter(valid_data['price'], valid_data['rating'], alpha=0.6)
                    axes[1, 0].set_title('Price vs Rating')
                    axes[1, 0].set_xlabel('Price ($)')
                    axes[1, 0].set_ylabel('Rating')
            
            # Category distribution
            if 'category' in df.columns:
                category_counts = df['category'].value_counts().head(10)
                axes[1, 1].bar(range(len(category_counts)), category_counts.values)
                axes[1, 1].set_title('Top Categories')
                axes[1, 1].set_xlabel('Category')
                axes[1, 1].set_ylabel('Number of Books')
                axes[1, 1].set_xticks(range(len(category_counts)))
                axes[1, 1].set_xticklabels(category_counts.index, rotation=45, ha='right')
            
            plt.tight_layout()
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Market visualization saved to {output_path}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating visualization: {e}")
            return False