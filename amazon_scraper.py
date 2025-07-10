"""
Amazon scraper module for KDP research automation
"""

import requests
import time
import re
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import pandas as pd
from urllib.parse import urljoin, quote
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AmazonScraper:
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.session.headers.update(HEADERS)
    
    def get_page(self, url, retries=RETRY_ATTEMPTS):
        """Fetch a webpage with retry logic"""
        for attempt in range(retries):
            try:
                # Rotate user agent
                self.session.headers['User-Agent'] = self.ua.random
                response = self.session.get(url, timeout=TIMEOUT)
                response.raise_for_status()
                time.sleep(REQUEST_DELAY)
                return response
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == retries - 1:
                    logger.error(f"Failed to fetch {url} after {retries} attempts")
                    return None
                time.sleep(REQUEST_DELAY * 2)
        return None
    
    def extract_book_data(self, book_element):
        """Extract book information from a book element"""
        try:
            # Title
            title_elem = book_element.find('h3') or book_element.find('h2')
            title = title_elem.get_text(strip=True) if title_elem else "N/A"
            
            # Author
            author_elem = book_element.find('span', class_='a-size-base') or book_element.find('a', class_='a-size-base')
            author = author_elem.get_text(strip=True) if author_elem else "N/A"
            
            # Price
            price_elem = book_element.find('span', class_='a-price-whole') or book_element.find('span', class_='a-offscreen')
            price_text = price_elem.get_text(strip=True) if price_elem else "0"
            price = self.extract_price(price_text)
            
            # Rating
            rating_elem = book_element.find('span', class_='a-icon-alt')
            rating = self.extract_rating(rating_elem.get_text() if rating_elem else "0")
            
            # Review count
            review_elem = book_element.find('span', class_='a-size-base')
            review_count = self.extract_review_count(review_elem.get_text() if review_elem else "0")
            
            # Rank (for bestseller lists)
            rank_elem = book_element.find('span', class_='zg-badge-text')
            rank = self.extract_rank(rank_elem.get_text() if rank_elem else "0")
            
            # Link
            link_elem = book_element.find('a', href=True)
            link = urljoin(AMAZON_BASE_URL, link_elem['href']) if link_elem else ""
            
            return {
                'title': title,
                'author': author,
                'price': price,
                'rating': rating,
                'review_count': review_count,
                'rank': rank,
                'link': link
            }
        except Exception as e:
            logger.error(f"Error extracting book data: {e}")
            return None
    
    def extract_price(self, price_text):
        """Extract numeric price from text"""
        try:
            price_match = re.search(r'[\d,]+\.?\d*', price_text.replace('$', '').replace(',', ''))
            return float(price_match.group()) if price_match else 0.0
        except:
            return 0.0
    
    def extract_rating(self, rating_text):
        """Extract numeric rating from text"""
        try:
            rating_match = re.search(r'(\d\.?\d*)', rating_text)
            return float(rating_match.group(1)) if rating_match else 0.0
        except:
            return 0.0
    
    def extract_review_count(self, review_text):
        """Extract review count from text"""
        try:
            # Remove commas and extract numbers
            review_match = re.search(r'([\d,]+)', review_text.replace(',', ''))
            return int(review_match.group(1)) if review_match else 0
        except:
            return 0
    
    def extract_rank(self, rank_text):
        """Extract rank number from text"""
        try:
            rank_match = re.search(r'#(\d+)', rank_text)
            return int(rank_match.group(1)) if rank_match else 0
        except:
            return 0
    
    def scrape_bestsellers(self, category=None, max_books=MAX_BOOKS_PER_CATEGORY):
        """Scrape Amazon bestseller lists"""
        logger.info(f"Scraping bestsellers for category: {category}")
        
        url = AMAZON_BESTSELLERS_URL
        if category:
            url = f"{url}/{category}"
        
        books = []
        page = 1
        
        while len(books) < max_books:
            page_url = f"{url}?pg={page}"
            response = self.get_page(page_url)
            
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            book_elements = soup.find_all('div', class_='zg-item-immersion')
            
            if not book_elements:
                logger.info("No more books found, stopping scrape")
                break
            
            for element in book_elements:
                if len(books) >= max_books:
                    break
                
                book_data = self.extract_book_data(element)
                if book_data:
                    book_data['category'] = category or 'general'
                    books.append(book_data)
            
            page += 1
            logger.info(f"Scraped page {page-1}, total books: {len(books)}")
        
        return books
    
    def search_books(self, keyword, max_books=50):
        """Search for books by keyword"""
        logger.info(f"Searching for books with keyword: {keyword}")
        
        search_url = f"{AMAZON_SEARCH_URL}?k={quote(keyword)}&i=stripbooks"
        books = []
        page = 1
        
        while len(books) < max_books:
            page_url = f"{search_url}&page={page}"
            response = self.get_page(page_url)
            
            if not response:
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            book_elements = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            if not book_elements:
                break
            
            for element in book_elements:
                if len(books) >= max_books:
                    break
                
                book_data = self.extract_book_data(element)
                if book_data:
                    book_data['search_keyword'] = keyword
                    books.append(book_data)
            
            page += 1
        
        return books
    
    def get_book_details(self, book_url):
        """Get detailed information about a specific book"""
        response = self.get_page(book_url)
        if not response:
            return None
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        try:
            # Description
            description_elem = soup.find('span', id='productDescription')
            description = description_elem.get_text(strip=True) if description_elem else ""
            
            # Categories/genres
            breadcrumb = soup.find('div', id='wayfinding-breadcrumbs_feature_div')
            categories = []
            if breadcrumb:
                category_links = breadcrumb.find_all('a')
                categories = [link.get_text(strip=True) for link in category_links]
            
            # Publication date
            pub_date_elem = soup.find('span', string=re.compile('Publication date'))
            pub_date = ""
            if pub_date_elem:
                pub_date = pub_date_elem.find_next('span').get_text(strip=True)
            
            # Page count
            page_count_elem = soup.find('span', string=re.compile('Print length'))
            page_count = 0
            if page_count_elem:
                page_text = page_count_elem.find_next('span').get_text()
                page_match = re.search(r'(\d+)', page_text)
                page_count = int(page_match.group(1)) if page_match else 0
            
            return {
                'description': description,
                'categories': categories,
                'publication_date': pub_date,
                'page_count': page_count
            }
        except Exception as e:
            logger.error(f"Error extracting book details: {e}")
            return None