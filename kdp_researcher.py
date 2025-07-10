#!/usr/bin/env python3
"""
Main KDP Research Automation Tool
Orchestrates all modules to provide comprehensive book market research
"""

import asyncio
import logging
import sys
from datetime import datetime
import click
from concurrent.futures import ThreadPoolExecutor
import time

from amazon_scraper import AmazonScraper
from keyword_researcher import KeywordResearcher
from market_analyzer import MarketAnalyzer
from report_generator import ReportGenerator
from config import *

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class KDPResearcher:
    def __init__(self):
        self.scraper = AmazonScraper()
        self.keyword_researcher = KeywordResearcher()
        self.market_analyzer = MarketAnalyzer()
        self.report_generator = ReportGenerator()
        self.all_books_data = []
        
    def run_comprehensive_research(self, categories=None, keywords=None, max_books_per_category=50):
        """Run complete market research analysis"""
        logger.info("🚀 Starting comprehensive KDP market research")
        start_time = time.time()
        
        try:
            # Step 1: Scrape bestseller data
            logger.info("📚 Step 1: Scraping Amazon bestseller data...")
            self.all_books_data = self._scrape_bestsellers(categories, max_books_per_category)
            
            if not self.all_books_data:
                logger.error("❌ No book data collected. Exiting.")
                return None
            
            logger.info(f"✅ Collected data for {len(self.all_books_data)} books")
            
            # Step 2: Keyword research and niche analysis
            logger.info("🔍 Step 2: Analyzing keywords and profitable niches...")
            keyword_data = self.keyword_researcher.extract_keywords_from_titles(self.all_books_data)
            profitable_niches = self.keyword_researcher.find_profitable_niches(self.all_books_data)
            
            # Step 3: Market analysis
            logger.info("📊 Step 3: Analyzing market trends and pricing...")
            market_trends = self.market_analyzer.analyze_market_trends(self.all_books_data)
            pricing_analysis = self.market_analyzer.analyze_pricing_strategies(self.all_books_data)
            market_insights = self.market_analyzer.generate_market_insights(self.all_books_data)
            
            # Step 4: Generate book ideas
            logger.info("💡 Step 4: Generating book ideas...")
            book_ideas = self.keyword_researcher.generate_book_ideas(profitable_niches)
            
            # Step 5: Create comprehensive reports
            logger.info("📝 Step 5: Generating comprehensive reports...")
            market_data = {
                **market_trends,
                'pricing_analysis': pricing_analysis,
                'insights': market_insights
            }
            
            reports = self.report_generator.generate_comprehensive_report(
                market_data, keyword_data, book_ideas, profitable_niches
            )
            
            # Step 6: Save raw data
            logger.info("💾 Step 6: Saving raw data...")
            self.report_generator.save_raw_data({
                'books_data': self.all_books_data,
                'keyword_data': keyword_data,
                'market_data': market_data,
                'profitable_niches': profitable_niches,
                'book_ideas': book_ideas
            })
            
            # Step 7: Create visualization
            viz_path = os.path.join(REPORTS_DIR, f"market_viz_{self.report_generator.timestamp}.png")
            self.market_analyzer.create_market_visualization(self.all_books_data, viz_path)
            
            end_time = time.time()
            duration = round(end_time - start_time, 2)
            
            logger.info(f"🎉 Research completed successfully in {duration} seconds!")
            
            # Return summary for display
            return {
                'summary': {
                    'total_books': len(self.all_books_data),
                    'profitable_niches_found': len(profitable_niches),
                    'book_ideas_generated': len(book_ideas),
                    'duration_seconds': duration
                },
                'top_niches': profitable_niches[:5],
                'top_book_ideas': book_ideas[:5],
                'reports': reports,
                'market_insights': market_insights[:5] if market_insights else []
            }
            
        except Exception as e:
            logger.error(f"❌ Error during research: {e}")
            return None
    
    def _scrape_bestsellers(self, categories, max_books_per_category):
        """Scrape bestseller data from specified categories"""
        all_books = []
        
        if not categories:
            categories = ['self-help', 'business-money', 'health-fitness-dieting', 'history']
        
        for category in categories:
            try:
                logger.info(f"📖 Scraping category: {category}")
                books = self.scraper.scrape_bestsellers(category, max_books_per_category)
                if books:
                    all_books.extend(books)
                    logger.info(f"✅ Found {len(books)} books in {category}")
                else:
                    logger.warning(f"⚠️ No books found in {category}")
                    
                # Polite delay between categories
                time.sleep(2)
                
            except Exception as e:
                logger.error(f"❌ Error scraping {category}: {e}")
                continue
        
        return all_books
    
    def research_specific_keywords(self, keywords, max_books_per_keyword=20):
        """Research specific keywords provided by user"""
        logger.info(f"🎯 Researching specific keywords: {keywords}")
        
        all_books = []
        for keyword in keywords:
            try:
                books = self.scraper.search_books(keyword, max_books_per_keyword)
                if books:
                    all_books.extend(books)
                    logger.info(f"✅ Found {len(books)} books for '{keyword}'")
                time.sleep(1)
            except Exception as e:
                logger.error(f"❌ Error researching '{keyword}': {e}")
        
        if all_books:
            self.all_books_data = all_books
            return self.run_analysis_only()
        else:
            logger.error("❌ No data found for provided keywords")
            return None
    
    def run_analysis_only(self):
        """Run analysis on existing data without scraping"""
        if not self.all_books_data:
            logger.error("❌ No book data available for analysis")
            return None
        
        logger.info("🔍 Running analysis on existing data...")
        
        # Analyze existing data
        keyword_data = self.keyword_researcher.extract_keywords_from_titles(self.all_books_data)
        profitable_niches = self.keyword_researcher.find_profitable_niches(self.all_books_data)
        market_trends = self.market_analyzer.analyze_market_trends(self.all_books_data)
        book_ideas = self.keyword_researcher.generate_book_ideas(profitable_niches)
        
        return {
            'keyword_data': keyword_data,
            'profitable_niches': profitable_niches,
            'market_trends': market_trends,
            'book_ideas': book_ideas
        }
    
    def quick_niche_check(self, niche_keyword):
        """Quick check for a specific niche"""
        logger.info(f"🔍 Quick niche analysis for: {niche_keyword}")
        
        try:
            books = self.scraper.search_books(niche_keyword, 30)
            if not books:
                return {"error": f"No books found for '{niche_keyword}'"}
            
            # Quick analysis
            analysis = self.keyword_researcher.analyze_keyword_competition(niche_keyword, books)
            
            return {
                'keyword': niche_keyword,
                'analysis': analysis,
                'sample_books': books[:5],
                'recommendation': self._get_niche_recommendation(analysis)
            }
            
        except Exception as e:
            logger.error(f"❌ Error in quick niche check: {e}")
            return {"error": str(e)}
    
    def _get_niche_recommendation(self, analysis):
        """Generate recommendation based on niche analysis"""
        competition = analysis.get('competition_level', 'Unknown')
        book_count = analysis.get('book_count', 0)
        avg_rating = analysis.get('avg_rating', 0)
        avg_price = analysis.get('avg_price', 0)
        
        if competition == 'Low' and book_count < 20:
            return "🟢 Excellent opportunity - Low competition, consider pursuing this niche"
        elif competition == 'Medium' and avg_rating < 4.0:
            return "🟡 Good opportunity - Medium competition but room for quality improvement"
        elif competition == 'High':
            return "🔴 High competition - Consider finding a more specific sub-niche"
        else:
            return "🟡 Moderate opportunity - Research deeper before committing"

# CLI Interface using Click
@click.group()
def cli():
    """🚀 KDP Research Automation Tool
    
    Automate your Amazon KDP market research and find profitable book opportunities.
    """
    pass

@cli.command()
@click.option('--categories', '-c', multiple=True, help='Categories to research (e.g., self-help, business-money)')
@click.option('--max-books', '-m', default=50, help='Maximum books per category (default: 50)')
@click.option('--output', '-o', help='Output directory for reports')
def research(categories, max_books, output):
    """🔍 Run comprehensive market research"""
    click.echo("🚀 Starting KDP market research...")
    
    researcher = KDPResearcher()
    
    # Convert categories tuple to list, use defaults if none provided
    categories_list = list(categories) if categories else None
    
    results = researcher.run_comprehensive_research(
        categories=categories_list,
        max_books_per_category=max_books
    )
    
    if results:
        click.echo("\n" + "="*60)
        click.echo("🎉 RESEARCH COMPLETED SUCCESSFULLY!")
        click.echo("="*60)
        
        summary = results['summary']
        click.echo(f"📊 Total books analyzed: {summary['total_books']}")
        click.echo(f"🎯 Profitable niches found: {summary['profitable_niches_found']}")
        click.echo(f"💡 Book ideas generated: {summary['book_ideas_generated']}")
        click.echo(f"⏱️ Duration: {summary['duration_seconds']} seconds")
        
        click.echo("\n🔍 TOP 3 PROFITABLE NICHES:")
        for i, niche in enumerate(results['top_niches'][:3], 1):
            click.echo(f"  {i}. {niche['keyword'].title()} (Score: {niche['profitability_score']}/100)")
        
        click.echo("\n💡 TOP 3 BOOK IDEAS:")
        for i, idea in enumerate(results['top_book_ideas'][:3], 1):
            click.echo(f"  {i}. {idea['title_idea']}")
        
        click.echo(f"\n📁 Reports saved in: {REPORTS_DIR}")
        click.echo("   - HTML report with visualizations")
        click.echo("   - Excel spreadsheet with data")
        click.echo("   - Text summary report")
        
    else:
        click.echo("❌ Research failed. Check logs for details.")

@cli.command()
@click.argument('keywords', nargs=-1, required=True)
@click.option('--max-books', '-m', default=20, help='Maximum books per keyword')
def keywords(keywords, max_books):
    """🎯 Research specific keywords"""
    click.echo(f"🔍 Researching keywords: {', '.join(keywords)}")
    
    researcher = KDPResearcher()
    results = researcher.research_specific_keywords(list(keywords), max_books)
    
    if results:
        click.echo("✅ Keyword research completed!")
        # Display results...
    else:
        click.echo("❌ Keyword research failed.")

@cli.command()
@click.argument('niche')
def quick_check(niche):
    """⚡ Quick analysis of a specific niche"""
    click.echo(f"⚡ Quick checking niche: {niche}")
    
    researcher = KDPResearcher()
    result = researcher.quick_niche_check(niche)
    
    if 'error' in result:
        click.echo(f"❌ {result['error']}")
        return
    
    analysis = result['analysis']
    click.echo(f"\n📊 NICHE ANALYSIS: {niche.title()}")
    click.echo(f"Competition Level: {analysis['competition_level']}")
    click.echo(f"Books Found: {analysis['book_count']}")
    click.echo(f"Average Rating: {analysis['avg_rating']}")
    click.echo(f"Average Price: ${analysis['avg_price']:.2f}")
    click.echo(f"Average Reviews: {analysis['avg_reviews']}")
    click.echo(f"\n{result['recommendation']}")

@cli.command()
def status():
    """📊 Check tool status and configuration"""
    click.echo("🔧 KDP Research Tool Status")
    click.echo(f"Output Directory: {OUTPUT_DIR}")
    click.echo(f"Reports Directory: {REPORTS_DIR}")
    click.echo(f"Data Directory: {DATA_DIR}")
    click.echo(f"Max Books per Category: {MAX_BOOKS_PER_CATEGORY}")
    click.echo(f"Target Price Range: ${TARGET_PRICE_RANGE[0]} - ${TARGET_PRICE_RANGE[1]}")
    click.echo("✅ Tool ready for use!")

if __name__ == "__main__":
    cli()