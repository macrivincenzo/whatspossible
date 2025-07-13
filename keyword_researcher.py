"""
Keyword research module for KDP book topics
"""

import requests
import pandas as pd
import nltk
from textblob import TextBlob
from collections import Counter
import re
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
except:
    pass

class KeywordResearcher:
    def __init__(self):
        self.popular_keywords = []
        self.trending_topics = []
    
    def extract_keywords_from_titles(self, books_data):
        """Extract popular keywords from book titles"""
        logger.info("Extracting keywords from book titles")
        
        all_titles = [book['title'].lower() for book in books_data if book.get('title')]
        title_text = ' '.join(all_titles)
        
        # Remove common words and punctuation
        stop_words = set(nltk.corpus.stopwords.words('english'))
        stop_words.update(['book', 'books', 'novel', 'story', 'guide', 'complete', 'ultimate'])
        
        # Extract words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title_text.lower())
        filtered_words = [word for word in words if word not in stop_words]
        
        # Count frequency
        word_freq = Counter(filtered_words)
        
        # Extract phrases (2-3 words)
        phrases = self.extract_phrases(all_titles)
        
        return {
            'single_words': word_freq.most_common(50),
            'phrases': phrases
        }
    
    def extract_phrases(self, titles):
        """Extract common phrases from titles"""
        phrase_counts = Counter()
        
        for title in titles:
            words = title.lower().split()
            
            # 2-word phrases
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                if len(phrase.replace(' ', '')) > 6:  # Ignore very short phrases
                    phrase_counts[phrase] += 1
            
            # 3-word phrases
            for i in range(len(words) - 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                if len(phrase.replace(' ', '')) > 10:
                    phrase_counts[phrase] += 1
        
        return phrase_counts.most_common(30)
    
    def analyze_keyword_competition(self, keyword, books_data):
        """Analyze competition level for a specific keyword"""
        keyword_books = [
            book for book in books_data 
            if keyword.lower() in book.get('title', '').lower()
        ]
        
        if not keyword_books:
            return {
                'competition_level': 'Low',
                'avg_rating': 0,
                'avg_reviews': 0,
                'avg_price': 0,
                'book_count': 0
            }
        
        ratings = [book['rating'] for book in keyword_books if book.get('rating', 0) > 0]
        reviews = [book['review_count'] for book in keyword_books if book.get('review_count', 0) > 0]
        prices = [book['price'] for book in keyword_books if book.get('price', 0) > 0]
        
        avg_rating = sum(ratings) / len(ratings) if ratings else 0
        avg_reviews = sum(reviews) / len(reviews) if reviews else 0
        avg_price = sum(prices) / len(prices) if prices else 0
        
        # Determine competition level
        book_count = len(keyword_books)
        if book_count > 100:
            competition = 'High'
        elif book_count > 50:
            competition = 'Medium'
        else:
            competition = 'Low'
        
        return {
            'competition_level': competition,
            'avg_rating': round(avg_rating, 2),
            'avg_reviews': int(avg_reviews),
            'avg_price': round(avg_price, 2),
            'book_count': book_count,
            'sample_books': keyword_books[:5]
        }
    
    def find_profitable_niches(self, books_data):
        """Identify potentially profitable niches based on data analysis"""
        logger.info("Analyzing profitable niches")
        
        # Extract keywords
        keywords_data = self.extract_keywords_from_titles(books_data)
        
        profitable_niches = []
        
        # Analyze top keywords
        for keyword, frequency in keywords_data['single_words'][:20]:
            competition_data = self.analyze_keyword_competition(keyword, books_data)
            
            # Calculate profitability score
            score = self.calculate_profitability_score(competition_data, frequency)
            
            profitable_niches.append({
                'keyword': keyword,
                'frequency': frequency,
                'profitability_score': score,
                **competition_data
            })
        
        # Sort by profitability score
        profitable_niches.sort(key=lambda x: x['profitability_score'], reverse=True)
        
        return profitable_niches[:10]
    
    def calculate_profitability_score(self, competition_data, frequency):
        """Calculate a profitability score for a keyword/niche"""
        # Factors: low competition, decent price, good ratings, reasonable frequency
        
        score = 0
        
        # Competition factor (lower is better)
        if competition_data['competition_level'] == 'Low':
            score += 40
        elif competition_data['competition_level'] == 'Medium':
            score += 20
        
        # Price factor (within target range is better)
        price = competition_data['avg_price']
        if TARGET_PRICE_RANGE[0] <= price <= TARGET_PRICE_RANGE[1]:
            score += 30
        elif price > 0:
            score += 10
        
        # Rating factor (higher is better)
        rating = competition_data['avg_rating']
        if rating >= 4.0:
            score += 20
        elif rating >= 3.5:
            score += 10
        
        # Frequency factor (moderate frequency is best)
        if 5 <= frequency <= 20:
            score += 20
        elif frequency > 20:
            score += 10
        
        # Review count factor (some reviews but not overwhelming)
        reviews = competition_data['avg_reviews']
        if 50 <= reviews <= 500:
            score += 15
        elif reviews > 0:
            score += 5
        
        return score
    
    def generate_book_ideas(self, profitable_niches, num_ideas=10):
        """Generate specific book ideas based on profitable niches"""
        logger.info("Generating book ideas")
        
        book_ideas = []
        
        for niche in profitable_niches[:5]:
            keyword = niche['keyword']
            
            # Generate different types of book ideas
            ideas = [
                f"The Complete Guide to {keyword.title()}",
                f"{keyword.title()} for Beginners: A Step-by-Step Approach",
                f"Advanced {keyword.title()}: Master the Art",
                f"The {keyword.title()} Workbook: Practical Exercises",
                f"{keyword.title()} Secrets: What Experts Don't Tell You",
                f"From Zero to {keyword.title()}: Your Journey Starts Here",
                f"The {keyword.title()} Blueprint: Proven Strategies",
                f"{keyword.title()} Made Simple: Easy Techniques"
            ]
            
            for idea in ideas[:2]:  # Take 2 ideas per niche
                book_ideas.append({
                    'title_idea': idea,
                    'niche': keyword,
                    'competition_level': niche['competition_level'],
                    'avg_price': niche['avg_price'],
                    'profitability_score': niche['profitability_score']
                })
        
        return book_ideas[:num_ideas]
    
    def research_trending_topics(self):
        """Research trending topics (placeholder for external API integration)"""
        # This would integrate with Google Trends API, social media APIs, etc.
        # For now, return some general trending topics in publishing
        
        trending_topics = [
            "mindfulness", "productivity", "remote work", "cryptocurrency",
            "sustainable living", "mental health", "artificial intelligence",
            "plant-based cooking", "home organization", "financial independence"
        ]
        
        return trending_topics
    
    def analyze_seasonal_trends(self, books_data):
        """Analyze seasonal patterns in book topics"""
        # This would analyze publication dates and seasonal keywords
        seasonal_keywords = {
            'spring': ['garden', 'fitness', 'renewal', 'fresh start'],
            'summer': ['travel', 'vacation', 'outdoor', 'adventure'],
            'fall': ['preparation', 'learning', 'cozy', 'harvest'],
            'winter': ['reflection', 'planning', 'indoor', 'holiday']
        }
        
        return seasonal_keywords