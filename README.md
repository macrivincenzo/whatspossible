# 📚 Amazon KDP Research Automation Tool

A comprehensive Python tool to automate market research for Amazon Kindle Direct Publishing (KDP). This tool helps authors and publishers discover profitable book niches, analyze competition, and generate data-driven book ideas.

## 🚀 Features

### 📊 Market Analysis
- **Bestseller Scraping**: Automatically scrape Amazon bestseller lists across multiple categories
- **Competition Analysis**: Analyze pricing strategies, ratings, and review counts
- **Market Trends**: Identify trending topics and seasonal patterns
- **Pricing Insights**: Find optimal price points based on market data

### 🔍 Keyword Research
- **Niche Discovery**: Find profitable, low-competition niches
- **Keyword Extraction**: Extract popular keywords from successful book titles
- **Competition Scoring**: Rate niches based on profitability potential
- **Book Idea Generation**: Automatically generate book title ideas for profitable niches

### 📝 Comprehensive Reports
- **Beautiful HTML Reports**: Interactive reports with visualizations
- **Excel Spreadsheets**: Detailed data analysis in spreadsheet format
- **Summary Reports**: Quick text summaries with key insights
- **Market Visualizations**: Charts and graphs showing market trends

### ⚡ Quick Analysis Tools
- **Niche Quick Check**: Rapidly analyze any specific niche or keyword
- **Keyword Research**: Research custom keywords and topics
- **Competitor Analysis**: Analyze specific books or authors

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Quick Setup

1. **Clone or download this repository**
```bash
git clone <repository-url>
cd kdp-research-tool
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment (optional)**
```bash
cp .env.example .env
# Edit .env file to add optional API keys
```

4. **Verify installation**
```bash
python kdp_researcher.py status
```

## 📖 Usage

### Command Line Interface

The tool provides a comprehensive CLI with multiple commands:

#### 🔍 Full Market Research
Run comprehensive market research across multiple categories:

```bash
# Research default categories (self-help, business, health, history)
python kdp_researcher.py research

# Research specific categories
python kdp_researcher.py research -c self-help -c business-money -c health-fitness-dieting

# Limit books per category
python kdp_researcher.py research -c self-help -m 30
```

#### 🎯 Keyword Research
Research specific keywords or topics:

```bash
# Research specific keywords
python kdp_researcher.py keywords "productivity" "mindfulness" "weight loss"

# Research with custom book limit
python kdp_researcher.py keywords "cryptocurrency" -m 25
```

#### ⚡ Quick Niche Check
Quickly analyze a specific niche:

```bash
# Quick analysis of a niche
python kdp_researcher.py quick-check "meditation"
python kdp_researcher.py quick-check "home organization"
```

#### 📊 Tool Status
Check tool configuration and status:

```bash
python kdp_researcher.py status
```

### Python API

You can also use the tool programmatically:

```python
from kdp_researcher import KDPResearcher

# Initialize the researcher
researcher = KDPResearcher()

# Run comprehensive research
results = researcher.run_comprehensive_research(
    categories=['self-help', 'business-money'],
    max_books_per_category=50
)

# Quick niche check
niche_analysis = researcher.quick_niche_check('productivity')

# Research specific keywords
keyword_results = researcher.research_specific_keywords(['mindfulness', 'meditation'])
```

## 📊 Output Files

The tool generates several types of output files in the `research_output/` directory:

### Reports Directory (`research_output/reports/`)
- **HTML Report**: `kdp_research_report_YYYYMMDD_HHMMSS.html`
  - Interactive dashboard with visualizations
  - Market overview metrics
  - Profitable niches table
  - Book ideas with scoring
  - Key insights and recommendations

- **Excel Report**: `kdp_research_data_YYYYMMDD_HHMMSS.xlsx`
  - Multiple sheets with detailed data
  - Market overview data
  - Profitable niches analysis
  - Book ideas list
  - Keyword frequency data

- **Summary Report**: `kdp_research_summary_YYYYMMDD_HHMMSS.txt`
  - Concise text summary
  - Top findings and recommendations
  - Action items and next steps

### Data Directory (`research_output/data/`)
- **Raw Data**: `kdp_raw_data_YYYYMMDD_HHMMSS.json`
  - Complete scraped data in JSON format
  - Useful for custom analysis or data processing

### Visualizations
- **Market Charts**: `market_viz_YYYYMMDD_HHMMSS.png`
  - Price distribution charts
  - Rating analysis
  - Category breakdowns

## 🎯 Understanding the Results

### Profitability Scores
The tool calculates profitability scores (0-100) based on:
- **Competition Level** (40 points max): Lower competition = higher score
- **Price Range** (30 points max): Books in target range ($2.99-$9.99) score higher
- **Rating Quality** (20 points max): Higher average ratings score better
- **Keyword Frequency** (20 points max): Moderate frequency is ideal
- **Review Count** (15 points max): Moderate review counts are preferred

### Competition Levels
- **Low**: Fewer than 50 books in the niche
- **Medium**: 50-100 books in the niche  
- **High**: More than 100 books in the niche

### Opportunity Classifications
- **🟢 High Opportunity** (70+ score): Excellent niches to pursue
- **🟡 Medium Opportunity** (50-69 score): Good niches with some competition
- **🔴 Low Opportunity** (<50 score): Highly competitive or saturated niches

## ⚙️ Configuration

### Basic Settings (config.py)
- `MAX_BOOKS_PER_CATEGORY`: Maximum books to analyze per category (default: 100)
- `TARGET_PRICE_RANGE`: Preferred price range for analysis (default: $2.99-$9.99)
- `MIN_RATING`: Minimum rating threshold (default: 3.5)
- `REQUEST_DELAY`: Delay between web requests (default: 1 second)

### Categories Available
The tool supports research across these Amazon categories:
- Fiction: literature-fiction, mystery-thriller-suspense, romance, science-fiction-fantasy
- Non-fiction: biographies-memoirs, business-money, health-fitness-dieting, self-help, history
- Children: childrens-books, teen-young-adult

## 🔧 Advanced Features

### Custom Analysis
Create custom analysis scripts using the individual modules:

```python
from amazon_scraper import AmazonScraper
from keyword_researcher import KeywordResearcher
from market_analyzer import MarketAnalyzer

# Custom scraping
scraper = AmazonScraper()
books = scraper.search_books("productivity", max_books=100)

# Custom keyword analysis
keyword_researcher = KeywordResearcher()
niches = keyword_researcher.find_profitable_niches(books)

# Custom market analysis
market_analyzer = MarketAnalyzer()
pricing = market_analyzer.analyze_pricing_strategies(books)
```

### Scheduling Research
Set up automated research runs using cron or task schedulers:

```bash
# Run daily research at 2 AM
0 2 * * * cd /path/to/kdp-tool && python kdp_researcher.py research
```

## 📈 Best Practices

### Research Strategy
1. **Start Broad**: Use comprehensive research to identify overall trends
2. **Focus on Opportunities**: Target niches with scores above 60
3. **Validate Manually**: Always manually verify top opportunities
4. **Track Over Time**: Run regular research to track market changes

### Book Development
1. **Quality First**: Focus on high-quality content for identified niches
2. **Competitive Pricing**: Use pricing insights to set competitive prices
3. **SEO Optimization**: Use discovered keywords in titles and descriptions
4. **Series Potential**: Consider series development for successful niches

### Market Analysis
1. **Multiple Categories**: Research across different categories for diversification
2. **Seasonal Trends**: Consider seasonal patterns in your chosen niches
3. **Competition Gaps**: Look for underserved sub-niches within popular categories
4. **Price Positioning**: Use market data to position your books effectively

## 🚨 Important Notes

### Ethical Use
- **Respect Rate Limits**: The tool includes delays to be respectful to Amazon's servers
- **No Automation on Amazon**: This tool is for research only, not for automated actions on Amazon
- **Copyright Respect**: Use insights to create original content, never copy existing works

### Legal Considerations
- **Web Scraping**: Tool scrapes publicly available data in compliance with robots.txt
- **Terms of Service**: Ensure your use complies with Amazon's Terms of Service
- **Data Usage**: Use collected data responsibly and in accordance with applicable laws

### Technical Limitations
- **Rate Limiting**: Amazon may temporarily block excessive requests
- **Data Accuracy**: Market data is a snapshot and may change rapidly
- **Category Changes**: Amazon occasionally updates category structures

## 🛠️ Troubleshooting

### Common Issues

**Error: "No books found"**
- Check your internet connection
- Verify category names are correct
- Try reducing the number of books per category

**Error: "Request failed"**
- Amazon may be rate limiting - wait and try again
- Check if Amazon's website structure has changed
- Verify your network settings

**Missing Dependencies**
```bash
pip install --upgrade -r requirements.txt
```

**Permission Errors**
- Ensure you have write permissions in the project directory
- Check that the output directories can be created

### Performance Optimization
- Use smaller `max_books` values for faster results
- Research fewer categories at once
- Run during off-peak hours for better success rates

## 🔮 Future Enhancements

### Planned Features
- [ ] Integration with Google Trends API for trending topics
- [ ] Social media keyword monitoring
- [ ] Competitor tracking and alerts
- [ ] A/B testing recommendations for titles and covers
- [ ] Sales rank prediction models
- [ ] Multi-language support
- [ ] Web dashboard interface

### Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For issues, questions, or feature requests:
1. Check the troubleshooting section above
2. Review existing issues in the repository
3. Create a new issue with detailed information about your problem

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Disclaimer

This tool is for research and educational purposes only. It provides market insights to help with decision-making but does not guarantee success in book publishing. Always conduct additional research and use your judgment when making business decisions.

The tool respects Amazon's robots.txt and implements respectful scraping practices. Users are responsible for ensuring their use complies with all applicable terms of service and laws.

---

**Happy researching and successful publishing! 📚✨**