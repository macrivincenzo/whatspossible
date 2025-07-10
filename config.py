"""
Configuration file for Amazon KDP Research Automation Tool
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Amazon URLs and endpoints
AMAZON_BASE_URL = "https://www.amazon.com"
AMAZON_BESTSELLERS_URL = "https://www.amazon.com/bestsellers/books"
AMAZON_SEARCH_URL = "https://www.amazon.com/s"

# Research categories for KDP
KDP_CATEGORIES = {
    "fiction": [
        "literature-fiction", "mystery-thriller-suspense", "romance", 
        "science-fiction-fantasy", "historical-fiction"
    ],
    "non_fiction": [
        "biographies-memoirs", "business-money", "health-fitness-dieting",
        "self-help", "history", "politics-social-sciences"
    ],
    "children": [
        "childrens-books", "teen-young-adult"
    ]
}

# Headers for web scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}

# Research parameters
MAX_BOOKS_PER_CATEGORY = 100
MIN_REVIEW_COUNT = 10
TARGET_PRICE_RANGE = (2.99, 9.99)
MIN_RATING = 3.5

# File paths
OUTPUT_DIR = "research_output"
REPORTS_DIR = os.path.join(OUTPUT_DIR, "reports")
DATA_DIR = os.path.join(OUTPUT_DIR, "data")

# Create directories if they don't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)

# API Keys (add to .env file)
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')

# Delay settings for polite scraping
REQUEST_DELAY = 1  # seconds between requests
RETRY_ATTEMPTS = 3
TIMEOUT = 30  # seconds