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
    """Test the astrology database with both base interpretations and video content."""
    # Initialize database with persistence
    data_dir = Path("../data")
    db = AstrologyDB(persist_dir=data_dir)
    bot = AstrologyBot(db)
    
    # Test queries for base interpretations
    base_queries = [
        "What does Sun in Aries mean?",
        "Tell me about Moon in Cancer",
        "What is the meaning of Venus square Mars?",
        "Describe the First House",
    ]
    
    logging.info("\nTesting base interpretation queries:")
    for query in base_queries:
        logging.info(f"\nQuery: {query}")
        logging.info("-" * 50)
        response = bot.process_query(query)
        logging.info(f"Response: {response}\n")
    
    # Test queries for video content
    video_queries = [
        "What are Saturn's effects in different houses?",
        "How does Saturn transit affect different signs?",
        "What is the significance of Saturn's direction?",
        "Tell me about Saturn's influence on career",
    ]
    
    logging.info("\nTesting video content queries:")
    for query in video_queries:
        logging.info(f"\nQuery: {query}")
        logging.info("-" * 50)
        response = bot.process_query(query)
        logging.info(f"Response: {response}\n")
    
    # Test combined knowledge queries
    combined_queries = [
        "How does Saturn in Aries affect the First House?",
        "What is the relationship between Moon phases and Saturn's transit?",
        "Tell me about Saturn's aspects with personal planets",
        "How do Saturn returns manifest in different houses?",
    ]
    
    logging.info("\nTesting combined knowledge queries:")
    for query in combined_queries:
        logging.info(f"\nQuery: {query}")
        logging.info("-" * 50)
        response = bot.process_query(query)
        logging.info(f"Response: {response}\n")

if __name__ == "__main__":
    test_database() 