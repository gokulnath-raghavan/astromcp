"""
Script to load processed video content into the astrology database.
"""

import json
from pathlib import Path
import logging
from database import AstrologyDB

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_video_content(db: AstrologyDB, content_file: Path):
    """Load processed video content into the database."""
    try:
        with open(content_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        logger.info(f"Loading {len(content)} segments into database...")
        
        for segment in content:
            db.add_interpretation(
                text=segment['text'],
                metadata=segment['metadata']
            )
            
        logger.info("Successfully loaded video content into database")
        
    except Exception as e:
        logger.error(f"Error loading video content: {e}")
        raise

def main():
    """Main function to load video content into database."""
    # Initialize database
    data_dir = Path("../data")
    db = AstrologyDB(persist_dir=data_dir)
    
    # Clear existing database
    logger.info("Clearing existing database...")
    db.clear_database()
    
    # Load video content
    content_file = data_dir / "video_content" / "processed_content.json"
    if not content_file.exists():
        logger.error(f"Processed content file not found at {content_file}")
        return
        
    load_video_content(db, content_file)

if __name__ == "__main__":
    main() 