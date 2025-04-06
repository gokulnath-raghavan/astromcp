import json
from database import AstrologyDB
from typing import List, Dict
import os

class DatabaseEnricher:
    def __init__(self, db: AstrologyDB):
        self.db = db
        self.knowledge_file = 'astrology_knowledge.json'
    
    def load_youtube_content(self) -> List[Dict]:
        """Load astrology content from YouTube processing."""
        if not os.path.exists(self.knowledge_file):
            print(f"No knowledge file found at {self.knowledge_file}")
            return []
        
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading knowledge file: {str(e)}")
            return []
    
    def process_content(self, content: Dict) -> Dict:
        """Process a single content item and prepare it for database insertion."""
        # Extract relevant information
        text = content['text']
        planet = content.get('planet')
        sign = content.get('sign')
        
        # Determine category based on content
        category = "General"
        if planet and sign:
            if planet.lower() in ['sun', 'moon']:
                category = f"{planet} Sign"
            else:
                category = "Planetary Position"
        elif "house" in text.lower():
            category = "House"
        elif any(word in text.lower() for word in ['conjunct', 'square', 'trine', 'opposition']):
            category = "Planetary Aspect"
        
        return {
            'text': text,
            'planet': planet,
            'sign': sign,
            'category': category,
            'source': 'youtube',
            'metadata': {
                'video_id': content.get('video_id'),
                'url': content.get('url'),
                'processed_at': content.get('processed_at')
            }
        }
    
    def enrich_database(self):
        """Enrich the database with YouTube content."""
        youtube_content = self.load_youtube_content()
        
        for video_data in youtube_content:
            for content in video_data.get('content', []):
                processed_content = self.process_content(content)
                
                # Add to database
                self.db.add_interpretation(
                    processed_content['text'],
                    {
                        'planet': processed_content['planet'],
                        'sign': processed_content['sign'],
                        'category': processed_content['category'],
                        'source': processed_content['source'],
                        'metadata': processed_content['metadata']
                    }
                )
        
        print("Database enrichment completed!")

def main():
    # Initialize database
    db = AstrologyDB()
    
    # Create enricher
    enricher = DatabaseEnricher(db)
    
    # Enrich database
    enricher.enrich_database()

if __name__ == "__main__":
    main() 