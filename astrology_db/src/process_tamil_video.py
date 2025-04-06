"""
Script to process Tamil astrology videos step by step.
"""

import logging
from pathlib import Path
from youtube_processor import YouTubeProcessor, download_subtitles, process_subtitles
from database import AstrologyDB
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_video(video_url: str, output_dir: Path, processor: YouTubeProcessor):
    """Process a Tamil astrology video step by step."""
    try:
        # Step 1: Download subtitles
        logger.info("\nStep 1: Downloading Tamil subtitles...")
        subtitle_path = download_subtitles(video_url, output_dir)
        logger.info(f"Subtitles downloaded to: {subtitle_path}")
        
        # Step 2: Get video transcript and translate
        logger.info("\nStep 2: Getting transcript and translating to English...")
        video_id = processor.extract_video_id(video_url)
        if not video_id:
            raise ValueError("Invalid YouTube URL")
            
        transcript = processor.get_transcript(video_id)
        if not transcript:
            raise ValueError("Failed to get transcript")
            
        # Save raw translated transcript
        raw_transcript_file = output_dir / f"{video_id}_raw_transcript.txt"
        with open(raw_transcript_file, 'w', encoding='utf-8') as f:
            f.write(transcript)
        logger.info(f"Raw translated transcript saved to: {raw_transcript_file}")
        
        # Step 3: Process and structure content
        logger.info("\nStep 3: Processing and structuring content...")
        content = process_subtitles(subtitle_path)
        
        # Save processed content
        processed_file = output_dir / f"{video_id}_processed.json"
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        logger.info(f"Processed {len(content)} segments")
        logger.info(f"Processed content saved to: {processed_file}")
        
        # Step 4: Analyze astrological content
        logger.info("\nStep 4: Analyzing astrological content...")
        content_stats = {
            'total_segments': len(content),
            'terms_found': {
                'planets': set(),
                'signs': set(),
                'houses': set(),
                'aspects': set(),
                'concepts': set()
            }
        }
        
        for segment in content:
            for category, terms in segment['metadata']['astrological_terms'].items():
                content_stats['terms_found'][category].update(terms)
        
        # Convert sets to lists for JSON serialization
        for category in content_stats['terms_found']:
            content_stats['terms_found'][category] = sorted(list(content_stats['terms_found'][category]))
        
        # Save content analysis
        analysis_file = output_dir / f"{video_id}_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(content_stats, f, indent=2)
        logger.info("Content analysis saved to: {analysis_file}")
        
        # Print summary
        logger.info("\nContent Summary:")
        logger.info(f"Total segments: {content_stats['total_segments']}")
        for category, terms in content_stats['terms_found'].items():
            logger.info(f"{category.capitalize()}: {', '.join(terms) if terms else 'None'}")
        
        return content
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise

def main():
    """Main function to process video and update database."""
    # Initialize
    data_dir = Path("../data")
    video_dir = data_dir / "video_content"
    video_dir.mkdir(parents=True, exist_ok=True)
    
    processor = YouTubeProcessor(cache_dir=str(video_dir))
    
    # Process video
    video_url = "https://youtu.be/bc7170FZK3s"  # Example Tamil astrology video
    content = process_video(video_url, video_dir, processor)
    
    # Update database
    db = AstrologyDB(persist_dir=data_dir)
    
    logger.info("\nUpdating database...")
    for segment in content:
        db.add_interpretation(
            text=segment['text'],
            metadata=segment['metadata']
        )
    
    logger.info("Database updated successfully")
    logger.info(f"Total entries in database: {db.get_size()}")

if __name__ == "__main__":
    main() 