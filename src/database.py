"""
Vector database for storing and retrieving astrological interpretations.
"""

import faiss
import numpy as np
from typing import List, Tuple, Dict, Any, Optional
from embeddings import AstrologyEmbeddings
import json
from pathlib import Path
import logging
from sentence_transformers import SentenceTransformer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AstrologyDB:
    """A vector database for storing and retrieving astrological interpretations.
    Uses FAISS for similarity search and stores metadata alongside text."""
    
    def __init__(self, persist_dir=None):
        """Initialize the database with optional persistence directory."""
        self.model = SentenceTransformer('all-mpnet-base-v2')
        self.texts = []
        self.metadata = []
        self.persist_dir = Path(persist_dir) if persist_dir else None
        
        # Initialize or load FAISS index
        if self.persist_dir and self.persist_dir.exists():
            self.load_from_disk()
        else:
            self.index = faiss.IndexFlatL2(768)  # 768 is the dimension of the embeddings
            if self.persist_dir:
                self.persist_dir.mkdir(parents=True, exist_ok=True)
    
    def add_interpretation(self, text, metadata=None):
        """Add a single interpretation with optional metadata."""
        if not text:
            return
            
        # Get embedding for the text
        embedding = self.model.encode([text])[0]
        
        # Add to FAISS index
        self.index.add(np.array([embedding]).astype('float32'))
        
        # Store text and metadata
        self.texts.append(text)
        self.metadata.append(metadata or {})
        
        # Save to disk if persistence is enabled
        if self.persist_dir:
            self.save_to_disk()
    
    def search(self, query, k=5, category=None, planet=None, sign=None):
        """Search for similar interpretations with optional filters."""
        if not self.texts:
            return []
            
        # Get query embedding
        query_embedding = self.model.encode([query])[0]
        
        # Search in FAISS index
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), len(self.texts))
        
        # Get results with scores and apply filters
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx >= len(self.texts):  # Skip invalid indices
                continue
                
            text = self.texts[idx]
            meta = self.metadata[idx]
            
            # Determine query type and apply appropriate filters
            query_lower = query.lower()
            
            # Handle house queries
            if 'house' in query_lower:
                if meta.get('category') != 'House':
                    continue
                # Extract house number if present
                if 'house' in meta:
                    house_num = meta['house']
                    if str(house_num) in query_lower:
                        results.append({
                            'text': text,
                            'metadata': meta,
                            'score': float(score)
                        })
                        continue
            
            # Handle planet queries
            if planet or any(p in query_lower for p in ['saturn', 'jupiter', 'mars', 'venus', 'mercury', 'sun', 'moon']):
                if meta.get('planet') == planet or meta.get('planet1') == planet or meta.get('planet2') == planet:
                    results.append({
                        'text': text,
                        'metadata': meta,
                        'score': float(score)
                    })
                    continue
            
            # Handle sign queries
            if sign or any(s in query_lower for s in ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']):
                if meta.get('sign') == sign or meta.get('ruling_sign') == sign:
                    results.append({
                        'text': text,
                        'metadata': meta,
                        'score': float(score)
                    })
                    continue
            
            # Handle aspect queries
            if any(a in query_lower for a in ['conjunct', 'square', 'trine', 'opposite', 'sextile']):
                if meta.get('category') == 'Planetary Aspect':
                    results.append({
                        'text': text,
                        'metadata': meta,
                        'score': float(score)
                    })
                    continue
            
            # If no specific filters matched, add to results
            if not (planet or sign or 'house' in query_lower):
                results.append({
                    'text': text,
                    'metadata': meta,
                    'score': float(score)
                })
            
        # Sort by score and return top k
        results.sort(key=lambda x: x['score'])
        return results[:k]
    
    def save_to_disk(self):
        """Save the database to disk."""
        if not self.persist_dir:
            return
            
        # Save FAISS index
        faiss.write_index(self.index, str(self.persist_dir / 'index.faiss'))
        
        # Save texts and metadata
        with open(self.persist_dir / 'data.json', 'w') as f:
            json.dump({'texts': self.texts, 'metadata': self.metadata}, f)
    
    def load_from_disk(self):
        """Load the database from disk."""
        if not self.persist_dir:
            return
            
        # Load FAISS index
        self.index = faiss.read_index(str(self.persist_dir / 'index.faiss'))
        
        # Load texts and metadata
        with open(self.persist_dir / 'data.json') as f:
            data = json.load(f)
            self.texts = data['texts']
            self.metadata = data['metadata']

def get_ordinal(n):
    """Convert number to ordinal string."""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}" 