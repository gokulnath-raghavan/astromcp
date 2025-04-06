from typing import List, Dict, Any, Optional
from database import AstrologyDB
from sentence_transformers import SentenceTransformer
import torch
from dotenv import load_dotenv
import os

class AstrologyBot:
    def __init__(self, db: Optional[AstrologyDB] = None):
        """Initialize the astrology bot.
        
        Args:
            db (Optional[AstrologyDB]): The vector database instance. If None, a new instance will be created.
        """
        # Initialize the text generation model
        self.model = SentenceTransformer('all-mpnet-base-v2')
        
        # Initialize or use provided database
        self.db = db if db is not None else AstrologyDB()
        
        load_dotenv()  # Load environment variables
        
    def get_relevant_interpretations(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Get relevant astrological interpretations from the vector database.
        
        Args:
            query (str): User's query
            k (int): Number of interpretations to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of relevant interpretations with metadata
        """
        try:
            # For complex queries involving multiple aspects, split into sub-queries
            query_parts = []
            query_lower = query.lower()
            words = query_lower.split()
            
            # Check for multiple aspects in the query
            aspects = []
            for aspect in ['sun', 'moon', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 'house']:
                if aspect in words:  # Check if the aspect is a complete word
                    aspects.append(aspect)
                    
            # If we have multiple aspects, search for each one
            if len(aspects) > 1:
                for aspect in aspects:
                    # Create a sub-query focusing on this aspect
                    aspect_idx = words.index(aspect)
                    
                    # Take a window of words around the aspect
                    start_idx = max(0, aspect_idx - 3)
                    end_idx = min(len(words), aspect_idx + 4)
                    sub_query = " ".join(words[start_idx:end_idx])
                    query_parts.append(sub_query)
            else:
                query_parts = [query]
                
            # Get interpretations for each query part
            all_results = []
            for part in query_parts:
                results = self.db.search(part, k=k)
                all_results.extend([
                    {
                        "text": text,
                        "score": score,
                        "metadata": metadata,
                        "query": part
                    }
                    for text, score, metadata in results
                ])
                
            # Sort by score and remove duplicates
            seen_texts = set()
            unique_results = []
            for result in sorted(all_results, key=lambda x: x['score'], reverse=True):
                if result['text'] not in seen_texts:
                    unique_results.append(result)
                    seen_texts.add(result['text'])
                    
            return unique_results[:k]
            
        except Exception as e:
            print(f"Error processing question: {str(e)}")
            # Fall back to simple search
            results = self.db.search(query, k=k)
            return [
                {
                    "text": text,
                    "score": score,
                    "metadata": metadata
                }
                for text, score, metadata in results
            ]
    
    def generate_response(self, query: str) -> str:
        """Generate a response based on relevant interpretations.
        
        Args:
            query (str): User's query
            
        Returns:
            str: Generated response
        """
        # Get relevant interpretations
        interpretations = self.get_relevant_interpretations(query, k=5)  # Get more interpretations for complex queries
        
        if not interpretations:
            return "I apologize, but I don't have enough information to provide a meaningful interpretation for your question."
        
        # For simple questions about a single aspect, use the most relevant interpretation
        if len(query.split()) < 8 or not any(word in query.lower() for word in ['and', 'with', 'affect', 'influence', 'between']):
            return interpretations[0]['text']
            
        # For complex questions, combine the most relevant interpretations
        response_parts = []
        seen_topics = set()  # Track topics we've covered to avoid redundancy
        
        # First, try to find interpretations that match multiple aspects
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        # Define important astrological terms to look for
        astro_terms = {
            # Planets
            'sun', 'moon', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto',
            'rahu', 'ketu',
            # Houses
            'house', 'ascendant', 'descendant', 'midheaven', 'ic',
            # Aspects
            'conjunction', 'opposition', 'square', 'trine', 'sextile',
            # Concepts
            'transit', 'retrograde', 'dasha', 'bhukti', 'period', 'phase',
            # Life Areas
            'career', 'relationship', 'love', 'marriage', 'family', 'money', 'health',
            'spiritual', 'growth', 'education', 'work', 'business'
        }
        
        # Find query-specific terms
        query_astro_terms = query_terms.intersection(astro_terms)
        
        # Sort interpretations by relevance to query terms
        scored_interpretations = []
        for interp in interpretations:
            text = interp['text'].lower()
            text_terms = set(text.split())
            
            # Calculate term overlap score
            common_terms = query_terms.intersection(text_terms)
            astro_common_terms = query_astro_terms.intersection(text_terms)
            
            # Calculate semantic similarity score
            semantic_score = interp['score']
            
            # Combine scores
            term_score = len(common_terms) / len(query_terms) if query_terms else 0
            astro_score = len(astro_common_terms) / len(query_astro_terms) if query_astro_terms else 0
            
            total_score = (semantic_score * 0.5 + term_score * 0.3 + astro_score * 0.2)
            scored_interpretations.append((interp, total_score))
        
        # Sort by total score
        scored_interpretations.sort(key=lambda x: x[1], reverse=True)
        
        # Build response from most relevant interpretations
        for interp, score in scored_interpretations:
            if score < 0.3:  # Lower threshold for including interpretations
                continue
                
            text = interp['text'].lower()
            text_terms = set(text.split())
            
            # Check if this interpretation adds new information
            new_terms = text_terms - seen_topics
            if new_terms:
                response_parts.append(interp['text'])
                seen_topics.update(text_terms)
                
        # If we have multiple relevant interpretations, combine them
        if len(response_parts) > 1:
            return " ".join(response_parts)
            
        # Fall back to the most relevant interpretation
        return interpretations[0]['text']
    
    def process_query(self, query: str) -> str:
        """Process a user query and return a response.
        
        Args:
            query (str): User's query
            
        Returns:
            str: Generated response
        """
        return self.generate_response(query) 