"""
Script to reprocess video content with improved cleaning.
"""

import json
from pathlib import Path
import logging
import re
from youtube_processor import clean_text
from database import AstrologyDB

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reprocess_content(input_file: Path, output_file: Path):
    """Reprocess video content with improved cleaning."""
    try:
        # Load original content
        with open(input_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        logger.info(f"Reprocessing {len(content)} segments...")
        
        # Process segments
        cleaned_content = []
        for segment in content:
            cleaned_text = clean_text(segment['text'])
            if cleaned_text:  # Only keep non-empty segments
                cleaned_content.append({
                    'text': cleaned_text,
                    'metadata': segment['metadata']
                })
                
        logger.info(f"Retained {len(cleaned_content)} segments after cleaning")
        
        # Save cleaned content
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(cleaned_content, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved cleaned content to {output_file}")
        
    except Exception as e:
        logger.error(f"Error reprocessing content: {e}")
        raise

def main():
    """Main function to reprocess content and rebuild database."""
    data_dir = Path("../data")
    input_file = data_dir / "video_content" / "processed_content.json"
    output_file = data_dir / "video_content" / "reprocessed_content.json"
    
    # Reprocess content
    reprocess_content(input_file, output_file)
    
    # Initialize and clear database
    db = AstrologyDB(persist_dir=data_dir)
    logger.info("Clearing existing database...")
    db.clear_database()
    
    # Load reprocessed content
    try:
        with open(output_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        logger.info(f"Loading {len(content)} segments into database...")
        
        for segment in content:
            db.add_interpretation(
                text=segment['text'],
                metadata=segment['metadata']
            )
            
        logger.info("Successfully rebuilt database with cleaned content")
        
    except Exception as e:
        logger.error(f"Error rebuilding database: {e}")
        raise

if __name__ == "__main__":
    main() 