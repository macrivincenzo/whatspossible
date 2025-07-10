#!/usr/bin/env python3
"""
Demo script for KDP Research Automation Tool
This script runs a simple demonstration of the tool's capabilities
"""

import logging
from kdp_researcher import KDPResearcher

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def run_demo():
    """Run a simple demonstration of the KDP research tool"""
    
    print("🚀 KDP Research Tool Demo")
    print("=" * 50)
    print("This demo will show you how the tool works with a quick niche analysis.")
    print()
    
    # Initialize the researcher
    print("📚 Initializing KDP Researcher...")
    researcher = KDPResearcher()
    
    # Demo 1: Quick niche check
    print("\n🔍 Demo 1: Quick Niche Analysis")
    print("-" * 30)
    
    demo_niches = ["productivity", "meditation", "cooking"]
    
    for niche in demo_niches:
        print(f"\n🎯 Analyzing niche: '{niche}'")
        result = researcher.quick_niche_check(niche)
        
        if 'error' in result:
            print(f"❌ {result['error']}")
            continue
            
        analysis = result['analysis']
        print(f"   📊 Competition Level: {analysis['competition_level']}")
        print(f"   📚 Books Found: {analysis['book_count']}")
        print(f"   ⭐ Average Rating: {analysis['avg_rating']}")
        print(f"   💰 Average Price: ${analysis['avg_price']:.2f}")
        print(f"   📝 Average Reviews: {analysis['avg_reviews']}")
        print(f"   💡 Recommendation: {result['recommendation']}")
    
    # Demo 2: Show sample book ideas
    print("\n\n💡 Demo 2: Book Idea Generation")
    print("-" * 35)
    print("Here are some example book ideas the tool might generate:")
    
    sample_ideas = [
        "The Complete Guide to Productivity",
        "Meditation for Beginners: A Step-by-Step Approach", 
        "Quick & Healthy Cooking: 30-Minute Meals",
        "The Minimalist Lifestyle: Declutter Your Life",
        "Home Organization Secrets: Professional Tips"
    ]
    
    for i, idea in enumerate(sample_ideas, 1):
        print(f"   {i}. {idea}")
    
    # Demo 3: Show report capabilities
    print("\n\n📊 Demo 3: Report Generation")
    print("-" * 30)
    print("The tool generates comprehensive reports including:")
    print("   📄 HTML Report - Interactive dashboard with charts")
    print("   📊 Excel Report - Detailed data analysis")
    print("   📝 Summary Report - Key insights and recommendations")
    print("   📈 Market Visualizations - Price and rating distributions")
    
    print("\n\n🎉 Demo Complete!")
    print("=" * 50)
    print("To run a full analysis, use:")
    print("   python kdp_researcher.py research")
    print("\nFor help and options:")
    print("   python kdp_researcher.py --help")
    print("\nHappy researching! 📚✨")

if __name__ == "__main__":
    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("Please check your installation and try again.")