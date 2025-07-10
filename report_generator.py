"""
Report generation module for KDP research
"""

import pandas as pd
from datetime import datetime
import os
import json
from tabulate import tabulate
import logging
from config import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ReportGenerator:
    def __init__(self):
        self.report_data = {}
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def generate_comprehensive_report(self, market_data, keyword_data, book_ideas, profitable_niches):
        """Generate a comprehensive research report"""
        logger.info("Generating comprehensive KDP research report")
        
        # Prepare report data
        report_data = {
            'metadata': {
                'generated_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'report_type': 'KDP Market Research',
                'version': '1.0'
            },
            'market_analysis': market_data,
            'keyword_analysis': keyword_data,
            'book_ideas': book_ideas,
            'profitable_niches': profitable_niches
        }
        
        # Generate different report formats
        html_report = self.create_html_report(report_data)
        excel_report = self.create_excel_report(report_data)
        summary_report = self.create_summary_report(report_data)
        
        return {
            'html_file': html_report,
            'excel_file': excel_report,
            'summary_file': summary_report,
            'timestamp': self.timestamp
        }
    
    def create_html_report(self, report_data):
        """Create HTML report with visualizations"""
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KDP Market Research Report</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f5f5f5;
                    color: #333;
                }}
                .container {{
                    max-width: 1200px;
                    margin: 0 auto;
                    background-color: white;
                    padding: 30px;
                    border-radius: 10px;
                    box-shadow: 0 0 20px rgba(0,0,0,0.1);
                }}
                h1 {{
                    color: #2c3e50;
                    text-align: center;
                    border-bottom: 3px solid #3498db;
                    padding-bottom: 10px;
                }}
                h2 {{
                    color: #34495e;
                    border-left: 4px solid #3498db;
                    padding-left: 15px;
                    margin-top: 30px;
                }}
                h3 {{
                    color: #2980b9;
                    margin-top: 25px;
                }}
                .metric-box {{
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    padding: 20px;
                    margin: 15px 0;
                    border-radius: 8px;
                    text-align: center;
                }}
                .metric-value {{
                    font-size: 2em;
                    font-weight: bold;
                    margin-bottom: 5px;
                }}
                .metric-label {{
                    font-size: 0.9em;
                    opacity: 0.9;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    background-color: white;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 12px;
                    text-align: left;
                }}
                th {{
                    background-color: #3498db;
                    color: white;
                    font-weight: bold;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
                .opportunity-high {{
                    background-color: #d4edda;
                    color: #155724;
                    padding: 5px 10px;
                    border-radius: 4px;
                }}
                .opportunity-medium {{
                    background-color: #fff3cd;
                    color: #856404;
                    padding: 5px 10px;
                    border-radius: 4px;
                }}
                .opportunity-low {{
                    background-color: #f8d7da;
                    color: #721c24;
                    padding: 5px 10px;
                    border-radius: 4px;
                }}
                .insight-box {{
                    background-color: #e8f4fd;
                    border-left: 4px solid #3498db;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 0 8px 8px 0;
                }}
                .book-idea {{
                    background-color: #f8f9fa;
                    border: 1px solid #e9ecef;
                    padding: 15px;
                    margin: 10px 0;
                    border-radius: 8px;
                }}
                .score-bar {{
                    background-color: #ecf0f1;
                    height: 20px;
                    border-radius: 10px;
                    overflow: hidden;
                    margin: 5px 0;
                }}
                .score-fill {{
                    background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60);
                    height: 100%;
                    transition: width 0.3s ease;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📚 Amazon KDP Market Research Report</h1>
                <p style="text-align: center; color: #7f8c8d; font-size: 1.1em;">
                    Generated on {report_data['metadata']['generated_at']}
                </p>
                
                <h2>📊 Market Overview</h2>
                {self._create_market_overview_html(report_data.get('market_analysis', {}))}
                
                <h2>🔍 Profitable Niches</h2>
                {self._create_niches_table_html(report_data.get('profitable_niches', []))}
                
                <h2>🎯 Book Ideas</h2>
                {self._create_book_ideas_html(report_data.get('book_ideas', []))}
                
                <h2>💡 Key Insights & Recommendations</h2>
                {self._create_insights_html(report_data)}
                
                <footer style="margin-top: 50px; text-align: center; color: #7f8c8d; border-top: 1px solid #ecf0f1; padding-top: 20px;">
                    <p>Generated by KDP Research Automation Tool</p>
                </footer>
            </div>
        </body>
        </html>
        """
        
        # Save HTML report
        html_filename = f"kdp_research_report_{self.timestamp}.html"
        html_path = os.path.join(REPORTS_DIR, html_filename)
        
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report saved: {html_path}")
        return html_path
    
    def _create_market_overview_html(self, market_data):
        """Create market overview section for HTML report"""
        if not market_data:
            return "<p>No market data available</p>"
        
        html = f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
            <div class="metric-box">
                <div class="metric-value">{market_data.get('total_books', 0)}</div>
                <div class="metric-label">Total Books Analyzed</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">${market_data.get('avg_price', 0):.2f}</div>
                <div class="metric-label">Average Price</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">{market_data.get('avg_rating', 0):.1f}</div>
                <div class="metric-label">Average Rating</div>
            </div>
            <div class="metric-box">
                <div class="metric-value">{int(market_data.get('avg_reviews', 0))}</div>
                <div class="metric-label">Average Reviews</div>
            </div>
        </div>
        """
        
        return html
    
    def _create_niches_table_html(self, niches):
        """Create profitable niches table for HTML report"""
        if not niches:
            return "<p>No niche data available</p>"
        
        html = """
        <table>
            <thead>
                <tr>
                    <th>Niche/Keyword</th>
                    <th>Profitability Score</th>
                    <th>Competition Level</th>
                    <th>Avg Price</th>
                    <th>Book Count</th>
                    <th>Opportunity</th>
                </tr>
            </thead>
            <tbody>
        """
        
        for niche in niches[:10]:
            score = niche.get('profitability_score', 0)
            score_width = min(100, score)
            
            if score >= 70:
                opportunity_class = "opportunity-high"
                opportunity_text = "High"
            elif score >= 50:
                opportunity_class = "opportunity-medium"
                opportunity_text = "Medium"
            else:
                opportunity_class = "opportunity-low"
                opportunity_text = "Low"
            
            html += f"""
            <tr>
                <td><strong>{niche.get('keyword', 'N/A').title()}</strong></td>
                <td>
                    <div class="score-bar">
                        <div class="score-fill" style="width: {score_width}%"></div>
                    </div>
                    {score}/100
                </td>
                <td>{niche.get('competition_level', 'Unknown')}</td>
                <td>${niche.get('avg_price', 0):.2f}</td>
                <td>{niche.get('book_count', 0)}</td>
                <td><span class="{opportunity_class}">{opportunity_text}</span></td>
            </tr>
            """
        
        html += "</tbody></table>"
        return html
    
    def _create_book_ideas_html(self, book_ideas):
        """Create book ideas section for HTML report"""
        if not book_ideas:
            return "<p>No book ideas generated</p>"
        
        html = ""
        for i, idea in enumerate(book_ideas[:10], 1):
            score = idea.get('profitability_score', 0)
            
            html += f"""
            <div class="book-idea">
                <h4>💡 Idea #{i}: {idea.get('title_idea', 'Untitled')}</h4>
                <p><strong>Niche:</strong> {idea.get('niche', 'General').title()}</p>
                <p><strong>Competition:</strong> {idea.get('competition_level', 'Unknown')}</p>
                <p><strong>Suggested Price:</strong> ${idea.get('avg_price', 0):.2f}</p>
                <p><strong>Opportunity Score:</strong> {score}/100</p>
            </div>
            """
        
        return html
    
    def _create_insights_html(self, report_data):
        """Create insights section for HTML report"""
        insights = []
        
        # Generate insights based on data
        market_data = report_data.get('market_analysis', {})
        niches = report_data.get('profitable_niches', [])
        
        if market_data:
            avg_price = market_data.get('avg_price', 0)
            if avg_price < 5:
                insights.append("💰 Consider premium pricing strategy - market is dominated by low-priced books")
            
            avg_rating = market_data.get('avg_rating', 0)
            if avg_rating < 4.0:
                insights.append("⭐ Focus on quality content - there's room for improvement in ratings")
        
        if niches:
            top_niche = niches[0]
            insights.append(f"🎯 Top opportunity: '{top_niche.get('keyword', '')}' niche with {top_niche.get('profitability_score', 0)}/100 score")
        
        # Default insights
        insights.extend([
            "📝 Research copyright-free content and trending topics",
            "🎨 Invest in professional cover design for better visibility",
            "📚 Consider creating series to build reader loyalty",
            "💡 Use keyword research for better discoverability"
        ])
        
        html = ""
        for insight in insights:
            html += f'<div class="insight-box">{insight}</div>'
        
        return html
    
    def create_excel_report(self, report_data):
        """Create Excel report with multiple sheets"""
        excel_filename = f"kdp_research_data_{self.timestamp}.xlsx"
        excel_path = os.path.join(REPORTS_DIR, excel_filename)
        
        try:
            with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
                # Market overview sheet
                if report_data.get('market_analysis'):
                    market_df = pd.DataFrame([report_data['market_analysis']])
                    market_df.to_excel(writer, sheet_name='Market Overview', index=False)
                
                # Profitable niches sheet
                if report_data.get('profitable_niches'):
                    niches_df = pd.DataFrame(report_data['profitable_niches'])
                    niches_df.to_excel(writer, sheet_name='Profitable Niches', index=False)
                
                # Book ideas sheet
                if report_data.get('book_ideas'):
                    ideas_df = pd.DataFrame(report_data['book_ideas'])
                    ideas_df.to_excel(writer, sheet_name='Book Ideas', index=False)
                
                # Keywords sheet
                if report_data.get('keyword_analysis'):
                    keywords_data = report_data['keyword_analysis']
                    if keywords_data.get('single_words'):
                        keywords_df = pd.DataFrame(keywords_data['single_words'], 
                                                   columns=['Keyword', 'Frequency'])
                        keywords_df.to_excel(writer, sheet_name='Keywords', index=False)
            
            logger.info(f"Excel report saved: {excel_path}")
            return excel_path
            
        except Exception as e:
            logger.error(f"Error creating Excel report: {e}")
            return None
    
    def create_summary_report(self, report_data):
        """Create a text summary report"""
        summary_filename = f"kdp_research_summary_{self.timestamp}.txt"
        summary_path = os.path.join(REPORTS_DIR, summary_filename)
        
        summary_content = f"""
KDP MARKET RESEARCH SUMMARY
Generated: {report_data['metadata']['generated_at']}
{'='*50}

MARKET OVERVIEW:
{'-'*20}
Total Books Analyzed: {report_data.get('market_analysis', {}).get('total_books', 0)}
Average Price: ${report_data.get('market_analysis', {}).get('avg_price', 0):.2f}
Average Rating: {report_data.get('market_analysis', {}).get('avg_rating', 0):.1f}/5.0
Average Reviews: {int(report_data.get('market_analysis', {}).get('avg_reviews', 0))}

TOP PROFITABLE NICHES:
{'-'*25}
"""
        
        # Add top niches
        niches = report_data.get('profitable_niches', [])
        for i, niche in enumerate(niches[:5], 1):
            summary_content += f"""
{i}. {niche.get('keyword', 'Unknown').title()}
   - Profitability Score: {niche.get('profitability_score', 0)}/100
   - Competition: {niche.get('competition_level', 'Unknown')}
   - Average Price: ${niche.get('avg_price', 0):.2f}
   - Book Count: {niche.get('book_count', 0)}
"""
        
        # Add top book ideas
        summary_content += f"""

TOP BOOK IDEAS:
{'-'*15}
"""
        
        book_ideas = report_data.get('book_ideas', [])
        for i, idea in enumerate(book_ideas[:5], 1):
            summary_content += f"""
{i}. {idea.get('title_idea', 'Untitled')}
   - Niche: {idea.get('niche', 'General').title()}
   - Competition: {idea.get('competition_level', 'Unknown')}
   - Opportunity Score: {idea.get('profitability_score', 0)}/100
"""
        
        summary_content += f"""

RECOMMENDATIONS:
{'-'*15}
• Focus on niches with profitability scores above 60
• Target price range: ${TARGET_PRICE_RANGE[0]} - ${TARGET_PRICE_RANGE[1]}
• Aim for topics with low to medium competition
• Ensure high-quality content to achieve ratings above 4.0
• Consider seasonal trends and trending topics
• Invest in professional editing and cover design

NEXT STEPS:
{'-'*11}
1. Validate top book ideas with target audience
2. Research content sources and outline structure
3. Analyze competitor books for content gaps
4. Plan marketing and launch strategy
5. Set up tracking for performance metrics
"""
        
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        
        logger.info(f"Summary report saved: {summary_path}")
        return summary_path
    
    def save_raw_data(self, all_data):
        """Save raw scraped data as JSON for future analysis"""
        data_filename = f"kdp_raw_data_{self.timestamp}.json"
        data_path = os.path.join(DATA_DIR, data_filename)
        
        try:
            with open(data_path, 'w', encoding='utf-8') as f:
                json.dump(all_data, f, indent=2, default=str)
            
            logger.info(f"Raw data saved: {data_path}")
            return data_path
            
        except Exception as e:
            logger.error(f"Error saving raw data: {e}")
            return None