"""
Script to process a specific YouTube video and add its content to the astrology database.
"""

from youtube_processor import YouTubeProcessor
from database import AstrologyDB
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Create cache and data directories
    cache_dir = Path("cache")
    data_dir = Path("data")
    cache_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Initialize processors
    youtube_processor = YouTubeProcessor(cache_dir=str(cache_dir))
    db = AstrologyDB(persist_dir=str(data_dir))
    
    # Process specific video
    video_url = "https://youtu.be/bc7170FZK3s"
    logger.info(f"Processing video: {video_url}")
    
    # Get video metadata and transcript
    metadata, transcript = youtube_processor.process_video(video_url)
    
    if metadata and transcript:
        logger.info("Successfully retrieved video content")
        
        # Extract astrological segments
        segments = youtube_processor.extract_astrological_segments(transcript)
        logger.info(f"Found {len(segments)} astrological segments")
        
        # Add segments to database
        for i, segment in enumerate(segments):
            # Prepare metadata
            metadata_entry = {
                "category": "YouTube Content",
                "source_url": video_url,
                "video_id": metadata["video_id"],
                **segment["metadata"]  # Include extracted astrological metadata
            }
            
            # Add to database
            db.add_interpretation(
                text=segment["text"],
                metadata=metadata_entry
            )
            
            # Log every 10th segment for verification
            if (i + 1) % 10 == 0:
                logger.info(f"Added segment {i+1}: {segment['text'][:100]}...")
            
        logger.info("Successfully added segments to database")
        
        # Test search functionality
        logger.info("\nTesting searches with new content:")
        logger.info("-" * 50)
        
        # Test queries
        test_queries = [
            "What does Saturn in Aries mean?",
            "Tell me about the 12th house",
            "What are the effects of Moon in Sagittarius?"
        ]
        
        for query in test_queries:
            logger.info(f"\nQuery: {query}")
            results = db.search(query, k=2)
            
            for text, score, metadata in results:
                logger.info(f"\nScore: {score:.3f}")
                logger.info(f"Text: {text}")
                logger.info(f"Source: {metadata.get('source_url', 'Database entry')}")
                logger.info("-" * 50)
    else:
        logger.error("Failed to process video")

if __name__ == "__main__":
    main() 