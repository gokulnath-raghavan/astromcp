"""
Module for processing YouTube videos and extracting astrological content.
"""

from typing import Dict, List, Optional, Tuple
import re
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import requests
from urllib.parse import urlparse, parse_qs
import json
from pathlib import Path
import logging
from deep_translator import GoogleTranslator
from tqdm import tqdm
import time
import yt_dlp

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class YouTubeProcessor:
    def __init__(self, cache_dir: Optional[str] = None):
        """Initialize the YouTube processor.
        
        Args:
            cache_dir (Optional[str]): Directory to cache transcripts and metadata
        """
        self.cache_dir = Path(cache_dir) if cache_dir else None
        if self.cache_dir:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            
        # Regular expression for extracting video IDs from various YouTube URL formats
        self.youtube_regex = re.compile(
            r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})'
        )
        
        # Initialize translator
        self.translator = GoogleTranslator(source='ta', target='en')
        
    def extract_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Optional[str]: Video ID if found, None otherwise
        """
        match = self.youtube_regex.search(url)
        return match.group(1) if match else None
        
    def get_video_metadata(self, video_id: str) -> Dict:
        """Get video metadata using YouTube Data API.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            Dict: Video metadata
        """
        # Check cache first
        if self.cache_dir:
            cache_file = self.cache_dir / f"{video_id}_metadata.json"
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    return json.load(f)
        
        # TODO: Implement YouTube Data API call
        # For now, return basic metadata
        metadata = {
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}"
        }
        
        # Cache metadata
        if self.cache_dir:
            with open(self.cache_dir / f"{video_id}_metadata.json", 'w') as f:
                json.dump(metadata, f)
                
        return metadata
        
    def translate_text(self, text: str, chunk_size: int = 1000, max_retries: int = 3) -> str:
        """Translate text with retries and chunking.
        
        Args:
            text (str): Text to translate
            chunk_size (int): Size of chunks to translate
            max_retries (int): Maximum number of retries per chunk
            
        Returns:
            str: Translated text
        """
        # Split text into chunks
        chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
        translated_chunks = []
        
        # Translate each chunk with progress bar
        with tqdm(total=len(chunks), desc="Translating") as pbar:
            for chunk in chunks:
                retries = 0
                while retries < max_retries:
                    try:
                        translated = self.translator.translate(chunk)
                        translated_chunks.append(translated)
                        break
                    except Exception as e:
                        retries += 1
                        if retries == max_retries:
                            logger.error(f"Failed to translate chunk after {max_retries} attempts: {str(e)}")
                            translated_chunks.append(chunk)
                        else:
                            logger.warning(f"Translation attempt {retries} failed, retrying...")
                            time.sleep(1)  # Wait before retrying
                pbar.update(1)
                
        return ' '.join(translated_chunks)
        
    def get_transcript(self, video_id: str) -> Optional[str]:
        """Get video transcript in Tamil and translate to English.
        
        Args:
            video_id (str): YouTube video ID
            
        Returns:
            Optional[str]: Translated transcript text if available, None otherwise
        """
        # Check cache first
        if self.cache_dir:
            cache_file = self.cache_dir / f"{video_id}_transcript.txt"
            if cache_file.exists():
                logger.info("Loading transcript from cache")
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return f.read()
        
        try:
            # Get Tamil transcript
            logger.info("Fetching Tamil transcript from YouTube")
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ta'])
            
            # Extract text and timestamps
            segments = []
            for entry in transcript_list:
                if isinstance(entry, dict) and 'text' in entry:
                    segments.append({
                        'text': entry['text'],
                        'start': entry.get('start', 0),
                        'duration': entry.get('duration', 0)
                    })
            
            # Combine nearby segments for better context during translation
            combined_segments = []
            current_text = []
            current_start = None
            
            for segment in segments:
                if not current_start:
                    current_start = segment['start']
                current_text.append(segment['text'])
                
                # Combine segments if total length is less than 200 characters
                if sum(len(t) for t in current_text) > 200:
                    combined_segments.append({
                        'text': ' '.join(current_text),
                        'start': current_start,
                    })
                    current_text = []
                    current_start = None
            
            # Add remaining text
            if current_text:
                combined_segments.append({
                    'text': ' '.join(current_text),
                    'start': current_start,
                })
            
            # Translate segments with progress tracking
            logger.info("Translating segments from Tamil to English")
            translated_segments = []
            
            with tqdm(total=len(combined_segments), desc="Translating") as pbar:
                for segment in combined_segments:
                    tamil_text = segment['text']
                    retries = 0
                    max_retries = 3
                    
                    while retries < max_retries:
                        try:
                            # Translate Tamil to English
                            translated_text = self.translator.translate(tamil_text)
                            
                            # Clean up common translation artifacts
                            translated_text = re.sub(r'\s+', ' ', translated_text)  # Normalize spaces
                            translated_text = re.sub(r'([.,!?])\s*\1+', r'\1', translated_text)  # Fix punctuation
                            
                            translated_segments.append({
                                'text': translated_text,
                                'start': segment['start']
                            })
                            break
                        except Exception as e:
                            retries += 1
                            if retries == max_retries:
                                logger.error(f"Failed to translate segment after {max_retries} attempts: {str(e)}")
                                translated_segments.append({
                                    'text': tamil_text,  # Keep original text if translation fails
                                    'start': segment['start']
                                })
                            else:
                                logger.warning(f"Translation attempt {retries} failed, retrying...")
                                time.sleep(2)  # Longer wait between retries
                    
                    pbar.update(1)
            
            # Combine all translated text
            translated_text = '\n'.join(segment['text'] for segment in translated_segments)
            
            # Cache the result
            if self.cache_dir:
                logger.info("Caching translated transcript")
                with open(cache_file, 'w', encoding='utf-8') as f:
                    f.write(translated_text)
            
            return translated_text
            
        except Exception as e:
            logger.error(f"Error getting transcript for video {video_id}: {str(e)}")
            return None
            
    def process_video(self, url: str) -> Tuple[Optional[Dict], Optional[str]]:
        """Process a YouTube video and extract content.
        
        Args:
            url (str): YouTube URL
            
        Returns:
            Tuple[Optional[Dict], Optional[str]]: Tuple of (metadata, transcript)
        """
        video_id = self.extract_video_id(url)
        if not video_id:
            logger.error(f"Invalid YouTube URL: {url}")
            return None, None
            
        metadata = self.get_video_metadata(video_id)
        transcript = self.get_transcript(video_id)
        
        return metadata, transcript
        
    def extract_astrological_segments(self, transcript: str) -> List[Dict[str, str]]:
        """Extract astrological segments from transcript.
        
        Args:
            transcript (str): Video transcript
            
        Returns:
            List[Dict[str, str]]: List of segments with astrological content
        """
        if not transcript:
            return []
            
        # Define astrological keywords and patterns
        zodiac_signs = r'(?:aries|taurus|gemini|cancer|leo|virgo|libra|scorpio|sagittarius|capricorn|aquarius|pisces)'
        planets = r'(?:sun|moon|mercury|venus|mars|jupiter|saturn|uranus|neptune|pluto)'
        aspects = r'(?:conjunction|opposition|trine|square|sextile)'
        houses = r'(?:1st|2nd|3rd|4th|5th|6th|7th|8th|9th|10th|11th|12th)\s+house'
        
        # Combine patterns
        pattern = f"(?i).*(?:{zodiac_signs}|{planets}|{aspects}|{houses}).*"
        
        # Split transcript into sentences and find matches
        sentences = re.split(r'[.!?]+', transcript)
        segments = []
        
        logger.info("Extracting astrological segments")
        for sentence in sentences:
            sentence = sentence.strip()
            if re.match(pattern, sentence):
                # Extract metadata
                metadata = {
                    "signs": re.findall(zodiac_signs, sentence, re.I),
                    "planets": re.findall(planets, sentence, re.I),
                    "aspects": re.findall(aspects, sentence, re.I),
                    "houses": re.findall(houses, sentence, re.I)
                }
                
                segments.append({
                    "text": sentence,
                    "metadata": metadata
                })
                
        logger.info(f"Found {len(segments)} astrological segments")
        return segments

def download_subtitles(video_url: str, output_dir: Path) -> str:
    """Download subtitles from a YouTube video."""
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
        'skip_download': True,
        'outtmpl': str(output_dir / '%(id)s.%(ext)s'),
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            video_id = info['id']
            subtitle_path = output_dir / f"{video_id}.en.vtt"
            return str(subtitle_path)
    except Exception as e:
        logger.error(f"Error downloading subtitles: {e}")
        raise

def clean_text(text: str) -> str:
    """Clean and normalize text content.
    
    Args:
        text (str): Raw text to clean
        
    Returns:
        str: Cleaned text
    """
    # Skip patterns for promotional and introductory content
    skip_patterns = [
        r'hello', r'welcome', r'greetings', r'thank you', r'goodbye',
        r'come and see', r'lot of details', r'please be patient',
        r'this is the video', r'this video is about',
        r'subscribe', r'like', r'click', r'watch', r'channel',
        r'www', r'http', r'com', r'net', r'org',
        r'follow', r'share', r'comment', r'notification',
        r'bell icon', r'ring the bell', r'hit the bell',
        r'join', r'membership', r'patreon', r'support',
        r'check out', r'look at', r'see more', r'learn more',
        r'stay tuned', r'keep watching', r'watch till the end',
        r'let me know', r'tell me', r'ask me', r'comment below',
        r'previous video', r'next video', r'other videos',
        r'playlist', r'series', r'part', r'episode',
        r'description', r'link', r'bio', r'profile',
        r'social media', r'facebook', r'instagram', r'twitter',
        r'telegram', r'whatsapp', r'group', r'community'
    ]
    
    # Skip if text matches any promotional pattern
    if any(re.search(pattern, text.lower()) for pattern in skip_patterns):
        return ""
        
    # Remove duplicate phrases
    words = text.split()
    unique_words = []
    seen_phrases = set()
    
    for i in range(len(words)):
        # Check 2-word phrases
        if i < len(words) - 1:
            phrase = f"{words[i]} {words[i+1]}"
            if phrase not in seen_phrases:
                unique_words.append(words[i])
                seen_phrases.add(phrase)
        else:
            unique_words.append(words[i])
            
    text = " ".join(unique_words)
    
    # Remove filler words and common phrases
    filler_words = {
        'um', 'uh', 'ah', 'eh', 'oh', 'well', 'like', 'you know',
        'sort of', 'kind of', 'basically', 'actually', 'literally',
        'pretty much', 'more or less', 'in a way', 'in some way',
        'in some sense', 'in some cases', 'in some situations',
        'in some circumstances', 'in some contexts', 'in some respects',
        'in some aspects', 'in some regards', 'in some ways',
        'in some manner', 'in some fashion', 'in some style',
        'in some form', 'in some shape', 'in some way shape or form',
        'in some way or another', 'in some way or other',
        'in some way or the other', 'in some way or another way',
        'in some way or another manner', 'in some way or another fashion',
        'in some way or another style', 'in some way or another form',
        'in some way or another shape', 'in some way or another way shape or form'
    }
    
    words = text.split()
    filtered_words = [word for word in words if word.lower() not in filler_words]
    text = " ".join(filtered_words)
    
    # Remove very short or generic segments
    if len(text.split()) < 5:
        return ""
        
    # Remove segments that are just questions without answers
    if text.endswith('?') and len(text.split()) < 8:
        return ""
        
    # Remove segments that are just statements about the video
    if any(phrase in text.lower() for phrase in ['this video', 'this time', 'today', 'now']):
        return ""
        
    # Remove segments that are just thank you or closing messages
    if any(phrase in text.lower() for phrase in ['thank you', 'thanks', 'goodbye', 'bye', 'see you']):
        return ""
        
    # Normalize spaces and punctuation
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'([.,!?])\s*', r'\1 ', text)
    text = text.strip()
    
    return text

def process_subtitles(subtitle_path: str) -> List[Dict]:
    """Process subtitle file into structured content."""
    content = []
    current_text = []
    current_timestamp = None
    
    # Define astrological keywords for content filtering
    astrological_terms = {
        'planets': ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 
                   'uranus', 'neptune', 'pluto', 'rahu', 'ketu'],
        'signs': ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 
                 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces'],
        'houses': [f'{i}th house' for i in range(1, 13)] + [f'{i}st house' for i in [1]] + 
                 [f'{i}nd house' for i in [2]] + [f'{i}rd house' for i in [3]],
        'aspects': ['conjunction', 'opposition', 'trine', 'square', 'sextile'],
        'concepts': ['transit', 'retrograde', 'direct', 'station', 'degree', 'sign', 
                    'ascendant', 'descendant', 'midheaven', 'nadir', 'natal', 'progression']
    }
    
    def has_astrological_content(text: str) -> bool:
        """Check if text contains astrological terms."""
        text_lower = text.lower()
        return any(term in text_lower 
                  for terms in astrological_terms.values() 
                  for term in terms)
    
    with open(subtitle_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Process each line
    for line in lines:
        line = line.strip()
        
        # Skip empty lines and metadata
        if not line or line.isdigit() or line.startswith(('WEBVTT', 'Kind:', 'Language:')):
            if current_text:
                text = ' '.join(current_text)
                # Only keep segments with astrological content
                if has_astrological_content(text):
                    cleaned_text = clean_text(text)
                    if cleaned_text:  # If text remains after cleaning
                        content.append({
                            'text': cleaned_text,
                            'metadata': {
                                'source': 'youtube',
                                'video_id': Path(subtitle_path).stem.split('.')[0],
                                'timestamp': current_timestamp,
                                'astrological_terms': {
                                    category: [term for term in terms 
                                             if term in cleaned_text.lower()]
                                    for category, terms in astrological_terms.items()
                                }
                            }
                        })
                current_text = []
                current_timestamp = None
            continue
        
        # Handle timestamp lines
        if '-->' in line:
            current_timestamp = line
            continue
        
        # Clean and add text
        line = re.sub(r'<[^>]+>', '', line)  # Remove HTML tags
        line = re.sub(r'\[.*?\]', '', line)  # Remove speaker labels
        line = line.strip()
        
        if line:
            current_text.append(line)
    
    # Process any remaining text
    if current_text:
        text = ' '.join(current_text)
        if has_astrological_content(text):
            cleaned_text = clean_text(text)
            if cleaned_text:
                content.append({
                    'text': cleaned_text,
                    'metadata': {
                        'source': 'youtube',
                        'video_id': Path(subtitle_path).stem.split('.')[0],
                        'timestamp': current_timestamp,
                        'astrological_terms': {
                            category: [term for term in terms 
                                     if term in cleaned_text.lower()]
                            for category, terms in astrological_terms.items()
                        }
                    }
                })
    
    # Combine related segments
    combined_content = []
    buffer = []
    
    for segment in content:
        if not buffer:
            buffer.append(segment)
            continue
        
        # Check if segments are related by astrological terms
        prev_terms = set(term 
                        for terms in buffer[-1]['metadata']['astrological_terms'].values() 
                        for term in terms)
        curr_terms = set(term 
                        for terms in segment['metadata']['astrological_terms'].values() 
                        for term in terms)
        
        # If segments share astrological terms and previous segment doesn't end with punctuation
        if prev_terms & curr_terms and not buffer[-1]['text'].rstrip()[-1] in '.!?':
            # Combine segments
            combined_text = clean_text(buffer[-1]['text'] + ' ' + segment['text'])
            if combined_text:
                buffer[-1]['text'] = combined_text
                buffer[-1]['metadata']['timestamp'] += ' + ' + segment['metadata']['timestamp']
                # Merge astrological terms
                for category in astrological_terms:
                    buffer[-1]['metadata']['astrological_terms'][category] = list(set(
                        buffer[-1]['metadata']['astrological_terms'].get(category, []) +
                        segment['metadata']['astrological_terms'].get(category, [])
                    ))
        else:
            # Start new segment
            buffer.append(segment)
        
        # If buffer has more than 2 segments or current segment ends with punctuation
        if len(buffer) > 2 or (buffer and buffer[-1]['text'].rstrip()[-1] in '.!?'):
            combined_content.extend(buffer[:-1])
            buffer = buffer[-1:]
    
    # Add remaining segments
    combined_content.extend(buffer)
    
    return combined_content

def main():
    """Main function to process YouTube video."""
    video_url = "https://youtu.be/bc7170FZK3s"
    output_dir = Path("../data/video_content")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Download subtitles
        logger.info("Downloading subtitles...")
        subtitle_path = download_subtitles(video_url, output_dir)
        
        # Process subtitles
        logger.info("Processing subtitles...")
        content = process_subtitles(subtitle_path)
        
        # Save processed content
        output_file = output_dir / "processed_content.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Processed {len(content)} segments")
        logger.info(f"Content saved to {output_file}")
        
    except Exception as e:
        logger.error(f"Error processing video: {e}")
        raise

if __name__ == "__main__":
    main() 