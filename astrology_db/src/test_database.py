"""
Test script for the astrology database functionality.
"""

import logging
from pathlib import Path
from database import AstrologyDB
from bot import AstrologyBot

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')

def test_database():
    """Test the astrology database with video content."""
    # Initialize database with persistence
    data_dir = Path("../data")
    db = AstrologyDB(persist_dir=data_dir)
    bot = AstrologyBot(db)
    
    # Test queries for video content
    video_queries = [
        "What are Saturn's effects in different houses?",
        "How does Saturn transit affect different signs?",
        "What is the significance of Saturn's direction?",
        "Tell me about Saturn's influence on career",
        "How does Saturn affect relationships?",
        "What are the effects of Saturn's retrograde?",
        "How does Saturn influence personal growth?",
        "Tell me about Saturn's role in spiritual development"
    ]
    
    logging.info("\nTesting video content queries:")
    for query in video_queries:
        logging.info(f"\nQuery: {query}")
        logging.info("-" * 50)
        response = bot.process_query(query)
        logging.info(f"Response: {response}\n")

if __name__ == "__main__":
    test_database() 