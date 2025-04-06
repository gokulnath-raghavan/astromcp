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
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AstrologyDB:
    def __init__(self, persist_dir: Optional[str] = None):
        """Initialize the vector database.
        
        Args:
            persist_dir (Optional[str]): Directory to persist the database
        """
        self.embeddings = AstrologyEmbeddings()
        self.dimension = self.embeddings.dimension
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts: List[str] = []
        self.metadata: List[Dict[str, Any]] = []
        self.persist_dir = Path(persist_dir) if persist_dir else None
        
        # Only try to load if the directory exists and contains the required files
        if (self.persist_dir and 
            self.persist_dir.exists() and 
            (self.persist_dir / "index.faiss").exists() and 
            (self.persist_dir / "data.json").exists()):
            logger.info("Loading database from disk")
            self.load_from_disk()
        else:
            # Add base interpretations only for new databases
            self._add_base_interpretations()
            
    def clear_database(self) -> None:
        """Clear all data from the database."""
        logger.info("Clearing database...")
        self.index = faiss.IndexFlatL2(self.dimension)
        self.texts = []
        self.metadata = []
        
        # Save empty database if persistence is enabled
        if self.persist_dir:
            self.save_to_disk()
            
        logger.info("Database cleared successfully")
        
    def _add_base_interpretations(self):
        """Add base astrological interpretations."""
        # Sun Signs
        sun_signs = {
            "Aries": "Sun in Aries represents leadership, initiative, and a pioneering spirit. This placement indicates strong willpower and natural confidence. Aries Sun individuals are often trailblazers who inspire others with their courage and determination.",
            "Taurus": "Sun in Taurus shows determination, practicality, and appreciation for beauty. This placement brings stability and material focus. Taurus Sun individuals are known for their reliability, patience, and strong connection to the physical world.",
            "Gemini": "Sun in Gemini indicates adaptability, communication skills, and intellectual curiosity. This placement brings versatility and social charm. Gemini Sun individuals are known for their quick wit, learning ability, and natural talent for networking.",
            "Cancer": "Sun in Cancer represents emotional depth, nurturing instincts, and strong intuition. This placement shows deep family ties and protective nature. Cancer Sun individuals are known for their emotional intelligence, caring nature, and strong connection to home and family."
        }
        
        for sign, interpretation in sun_signs.items():
            self.add_interpretation(interpretation, {
                "planet": "Sun",
                "sign": sign,
                "category": "Sun Sign",
                "element": "Fire" if sign in ["Aries", "Leo", "Sagittarius"] else
                          "Earth" if sign in ["Taurus", "Virgo", "Capricorn"] else
                          "Air" if sign in ["Gemini", "Libra", "Aquarius"] else "Water",
                "modality": "Cardinal" if sign in ["Aries", "Cancer", "Libra", "Capricorn"] else
                           "Fixed" if sign in ["Taurus", "Leo", "Scorpio", "Aquarius"] else "Mutable",
                "ruling_planet": "Mars" if sign == "Aries" else
                                "Venus" if sign == "Taurus" else
                                "Mercury" if sign == "Gemini" else "Moon"
            })
            
        # Moon Signs
        moon_signs = {
            "Cancer": "Moon in Cancer indicates emotional sensitivity and strong nurturing instincts. This placement shows deep emotional intelligence and a natural ability to care for others. Cancer Moon individuals are highly intuitive and deeply connected to their family and home.",
            "Leo": "Moon in Leo brings emotional warmth, creativity, and a desire for recognition. This placement indicates a need for emotional expression and dramatic flair. Leo Moon individuals are generous with their emotions and seek appreciation for their caring nature.",
            "Virgo": "Moon in Virgo shows emotional practicality and analytical thinking. This placement indicates a need for order and service to others. Virgo Moon individuals process emotions through practical problem-solving and find comfort in being helpful.",
            "Libra": "Moon in Libra brings emotional harmony and relationship focus. This placement indicates a need for balance and partnership. Libra Moon individuals process emotions through relationships and seek peace and beauty in their emotional environment."
        }
        
        for sign, interpretation in moon_signs.items():
            self.add_interpretation(interpretation, {
                "planet": "Moon",
                "sign": sign,
                "category": "Moon Sign",
                "element": "Fire" if sign in ["Aries", "Leo", "Sagittarius"] else
                          "Earth" if sign in ["Taurus", "Virgo", "Capricorn"] else
                          "Air" if sign in ["Gemini", "Libra", "Aquarius"] else "Water",
                "modality": "Cardinal" if sign in ["Aries", "Cancer", "Libra", "Capricorn"] else
                           "Fixed" if sign in ["Taurus", "Leo", "Scorpio", "Aquarius"] else "Mutable",
                "ruling_planet": "Moon" if sign == "Cancer" else
                                "Sun" if sign == "Leo" else
                                "Mercury" if sign == "Virgo" else "Venus"
            })
            
        # Aspects
        aspects = {
            "Sun conjunct Moon": {
                "text": "Sun conjunct Moon represents a strong alignment between conscious and unconscious drives. This aspect indicates emotional harmony and clear self-expression. Individuals with this aspect often have a strong sense of self and clear emotional awareness.",
                "planet1": "Sun",
                "planet2": "Moon",
                "aspect": "conjunct",
                "orb": "0-10 degrees"
            },
            "Venus square Mars": {
                "text": "Venus square Mars indicates tension between love and desire. This aspect often brings passionate relationships but may also indicate challenges in balancing romance and physical attraction. Individuals with this aspect may experience internal conflicts between their values and desires.",
                "planet1": "Venus",
                "planet2": "Mars",
                "aspect": "square",
                "orb": "0-8 degrees"
            },
            "Jupiter trine Saturn": {
                "text": "Jupiter trine Saturn represents a harmonious balance between expansion and limitation. This aspect indicates good judgment and the ability to achieve long-term goals. Individuals with this aspect often have a natural talent for planning and execution.",
                "planet1": "Jupiter",
                "planet2": "Saturn",
                "aspect": "trine",
                "orb": "0-8 degrees"
            },
            "Mercury opposite Neptune": {
                "text": "Mercury opposite Neptune can indicate confusion between reality and imagination. This aspect often brings creative thinking but may also lead to misunderstandings. Individuals with this aspect may need to work on grounding their thoughts in reality.",
                "planet1": "Mercury",
                "planet2": "Neptune",
                "aspect": "opposite",
                "orb": "0-8 degrees"
            }
        }
        
        for name, data in aspects.items():
            self.add_interpretation(data["text"], {
                "planet1": data["planet1"],
                "planet2": data["planet2"],
                "aspect": data["aspect"],
                "category": "Planetary Aspect",
                "orb": data["orb"]
            })
            
        # Houses
        houses = {
            1: "First House represents the self, personality, and physical appearance. This house shows how you present yourself to the world and your approach to new beginnings. Planets in the First House strongly influence your personality and life path.",
            2: "Second House indicates values, possessions, and self-worth. This house shows your relationship with money, resources, and personal values. Planets in the Second House influence your financial matters and sense of self-worth.",
            3: "Third House represents communication, siblings, and short-distance travel. This house shows your learning style and how you process information. Planets in the Third House influence your communication abilities and relationships with siblings.",
            4: "Fourth House indicates home, family, and emotional foundation. This house shows your roots and sense of security. Planets in the Fourth House influence your home life, family relationships, and emotional well-being."
        }
        
        for house_num, interpretation in houses.items():
            self.add_interpretation(interpretation, {
                "house": house_num,
                "category": "House",
                "ruling_sign": "Aries" if house_num == 1 else
                              "Taurus" if house_num == 2 else
                              "Gemini" if house_num == 3 else "Cancer",
                "ruling_planet": "Mars" if house_num == 1 else
                                "Venus" if house_num == 2 else
                                "Mercury" if house_num == 3 else "Moon",
                "natural_house": "Angular" if house_num in [1, 4, 7, 10] else
                                "Succedent" if house_num in [2, 5, 8, 11] else "Cadent"
            })
            
    def add_interpretation(self, text: str, metadata: Dict[str, Any] = None) -> None:
        """Add an astrological interpretation to the database.
        
        Args:
            text (str): The interpretation text
            metadata (Dict[str, Any], optional): Additional metadata
        """
        # Generate and normalize embedding
        embedding = self.embeddings.generate_embedding(text)
        normalized_embedding = self.embeddings.normalize_embeddings(embedding)
        
        # Add to FAISS index
        self.index.add(normalized_embedding.astype('float32'))
        
        # Store text and metadata
        self.texts.append(text)
        self.metadata.append(metadata or {})
        
        # Log the addition
        logger.debug(f"Added interpretation: {text[:100]}...")
        
        # Persist if directory is set
        if self.persist_dir:
            self.save_to_disk()
            
    def search(self, query: str, k: int = 5, 
              category: Optional[str] = None,
              planet: Optional[str] = None,
              sign: Optional[str] = None) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for interpretations matching the query.
        
        Args:
            query (str): Search query
            k (int): Number of results to return
            category (Optional[str]): Filter by category (e.g., "Sun Sign", "Moon Sign")
            planet (Optional[str]): Filter by planet
            sign (Optional[str]): Filter by zodiac sign
            
        Returns:
            List[Tuple[str, float, Dict[str, Any]]]: List of (text, score, metadata) tuples
        """
        # Generate query embedding
        query_embedding = self.embeddings.generate_embedding(query)
        normalized_query = self.embeddings.normalize_embeddings(query_embedding)
        
        # Search in FAISS index with more results to allow for filtering
        k_search = min(k * 10, len(self.texts))  # Get even more results for better filtering
        distances, indices = self.index.search(normalized_query.astype('float32').reshape(1, -1), k_search)
        
        # Convert distances to similarities
        max_distance = np.max(distances) if len(distances) > 0 and len(distances[0]) > 0 else 1.0
        similarities = 1 - (distances / max_distance if max_distance > 0 else distances)
        
        # Extract key terms from query
        query_terms = set(query.lower().split())
        important_terms = {
            # Planets
            'saturn', 'jupiter', 'mars', 'venus', 'mercury', 'moon', 'sun', 'rahu', 'ketu',
            # Aspects
            'retrograde', 'transit', 'conjunction', 'opposition', 'square', 'trine', 'sextile',
            # Houses and Signs
            'house', 'sign', 'ascendant', 'descendant', 'midheaven', 'ic',
            # Concepts
            'aspect', 'career', 'relationship', 'money', 'health', 'spiritual', 'growth',
            # Life Areas
            'love', 'marriage', 'family', 'friends', 'work', 'business', 'education',
            # Timing
            'period', 'phase', 'cycle', 'return', 'dasha', 'bhukti'
        }
        query_important_terms = query_terms.intersection(important_terms)
        
        # Define promotional and generic content patterns
        promotional_patterns = [
            r'subscribe', r'like', r'click', r'watch', r'video', r'channel',
            r'welcome', r'hello', r'greetings', r'thank you', r'goodbye',
            r'come and see', r'lot of details', r'please be patient',
            r'this is the video', r'this video is about'
        ]
        
        # Collect results with metadata filtering and enhanced scoring
        results = []
        for idx, (distance, similarity) in enumerate(zip(distances[0], similarities[0])):
            if idx >= len(self.texts):
                continue
                
            metadata = self.metadata[idx]
            text = self.texts[idx]
            text_lower = text.lower()
            
            # Skip very short or generic segments
            if len(text.split()) < 5:
                logger.debug(f"Skipping short text: {text[:100]}...")
                continue
                
            # Apply metadata filters
            if category and metadata.get('category') != category:
                logger.debug(f"Skipping category mismatch: {text[:100]}...")
                continue
            if planet and metadata.get('planet') != planet and metadata.get('planet1') != planet and metadata.get('planet2') != planet:
                logger.debug(f"Skipping planet mismatch: {text[:100]}...")
                continue
            if sign and metadata.get('sign') != sign:
                logger.debug(f"Skipping sign mismatch: {text[:100]}...")
                continue
            
            # Skip promotional or generic content
            if any(re.search(pattern, text_lower) for pattern in promotional_patterns):
                logger.debug(f"Skipping promotional content: {text[:100]}...")
                continue
            
            # Calculate term overlap score
            text_terms = set(text_lower.split())
            common_terms = query_terms.intersection(text_terms)
            important_common_terms = query_important_terms.intersection(text_terms)
            
            # Calculate adjusted similarity score
            adjusted_similarity = similarity
            
            # Boost score based on content quality
            word_count = len(text.split())
            if word_count > 15:  # Favor longer, more detailed segments
                adjusted_similarity *= 1.2
            if word_count > 30:  # Additional boost for very detailed segments
                adjusted_similarity *= 1.1
            
            # Boost score based on term overlap
            if common_terms:
                term_overlap_score = len(common_terms) / len(query_terms)
                adjusted_similarity *= (1 + 0.3 * term_overlap_score)
            
            # Extra boost for important astrological terms
            if important_common_terms:
                adjusted_similarity *= (1 + 0.4 * len(important_common_terms))
            
            # Boost score for exact matches of important terms
            exact_matches = sum(1 for term in query_important_terms if term in text_lower)
            if exact_matches:
                adjusted_similarity *= (1 + 0.2 * exact_matches)
            
            # Log scoring details
            logger.debug(f"Text: {text[:100]}...")
            logger.debug(f"Base similarity: {similarity:.3f}")
            logger.debug(f"Word count: {word_count}")
            logger.debug(f"Common terms: {common_terms}")
            logger.debug(f"Important common terms: {important_common_terms}")
            logger.debug(f"Exact matches: {exact_matches}")
            logger.debug(f"Adjusted similarity: {adjusted_similarity:.3f}")
            
            # Add result if score is above threshold
            if adjusted_similarity > 0.3:  # Lowered threshold for better recall
                results.append((text, float(adjusted_similarity), metadata))
            else:
                logger.debug(f"Skipping low similarity: {text[:100]}...")
        
        # Sort by adjusted similarity score
        results.sort(key=lambda x: x[1], reverse=True)
        
        # Log search results
        logger.info(f"Found {len(results)} results for query: {query}")
        if results:
            logger.info(f"Top result (score: {results[0][1]:.3f}): {results[0][0][:100]}...")
        
        return results[:k]
        
    def search_by_metadata(self, metadata_filters: Dict[str, Any], k: int = 5) -> List[Tuple[str, float, Dict[str, Any]]]:
        """Search for interpretations matching specific metadata criteria.
        
        Args:
            metadata_filters (Dict[str, Any]): Dictionary of metadata filters
            k (int): Number of results to return
            
        Returns:
            List[Tuple[str, float, Dict[str, Any]]]: List of (text, score, metadata) tuples
        """
        results = []
        for text, metadata in zip(self.texts, self.metadata):
            # Check if all filters match
            matches = all(metadata.get(k) == v for k, v in metadata_filters.items())
            if matches:
                # Generate a similarity score based on metadata match
                score = 1.0  # Perfect match
                results.append((text, score, metadata))
                
        # Sort by score and return top k
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
    
    def save_to_disk(self) -> None:
        """Save the database to disk."""
        if not self.persist_dir:
            return
            
        # Create directory if it doesn't exist
        self.persist_dir.mkdir(parents=True, exist_ok=True)
            
        # Save FAISS index
        faiss.write_index(self.index, str(self.persist_dir / "index.faiss"))
        
        # Save texts and metadata
        data = {
            "texts": self.texts,
            "metadata": self.metadata
        }
        with open(self.persist_dir / "data.json", 'w') as f:
            json.dump(data, f)
            
        logger.info(f"Saved database to {self.persist_dir}")
        
    def load_from_disk(self) -> None:
        """Load the database from disk."""
        if not self.persist_dir:
            return
            
        # Load FAISS index
        self.index = faiss.read_index(str(self.persist_dir / "index.faiss"))
        
        # Load texts and metadata
        with open(self.persist_dir / "data.json", 'r') as f:
            data = json.load(f)
            self.texts = data["texts"]
            self.metadata = data["metadata"]
            
        logger.info(f"Loaded database from {self.persist_dir} with {len(self.texts)} entries")
            
    def batch_add(self, texts: List[str], metadata_list: List[Dict[str, Any]] = None) -> None:
        """Add multiple interpretations at once.
        
        Args:
            texts (List[str]): List of interpretation texts
            metadata_list (List[Dict[str, Any]], optional): List of metadata dictionaries
        """
        if metadata_list is None:
            metadata_list = [{} for _ in texts]
            
        for text, metadata in zip(texts, metadata_list):
            self.add_interpretation(text, metadata)
            
    def get_size(self) -> int:
        """Get the number of interpretations in the database.
        
        Returns:
            int: Number of stored interpretations
        """
        return len(self.texts) 