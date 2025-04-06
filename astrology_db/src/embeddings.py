from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
import re

class AstrologyEmbeddings:
    def __init__(self, model_name: str = 'all-mpnet-base-v2'):
        """Initialize the embedding model.
        
        Args:
            model_name (str): Name of the sentence transformer model to use
        """
        self.model = SentenceTransformer(model_name)
        self.dimension = 768  # Dimension for all-mpnet-base-v2 model
        
    def preprocess_text(self, text: str) -> str:
        """Preprocess text for astrological context.
        
        Args:
            text (str): Input text
            
        Returns:
            str: Preprocessed text
        """
        # Standardize astrological terms
        text = re.sub(r'(\w+)\s+in\s+(\w+)', r'\1_in_\2', text)  # e.g., "Sun in Leo" -> "Sun_in_Leo"
        text = re.sub(r'(\w+)\s+(conjunct|square|trine|opposite|sextile)\s+(\w+)', r'\1_\2_\3', text)  # e.g., "Sun conjunct Moon" -> "Sun_conjunct_Moon"
        text = re.sub(r'(\d+)(st|nd|rd|th)\s+House', r'House_\1', text)  # e.g., "1st House" -> "House_1"
        
        # Add context markers
        if "House" in text:
            text = f"[HOUSE] {text}"
        elif any(aspect in text.lower() for aspect in ["conjunct", "square", "trine", "opposite", "sextile"]):
            text = f"[ASPECT] {text}"
        elif any(planet in text for planet in ["Sun", "Moon", "Mercury", "Venus", "Mars", "Jupiter", "Saturn"]):
            text = f"[PLANET] {text}"
            
        return text
        
    def generate_embedding(self, text: Union[str, List[str]]) -> np.ndarray:
        """Generate embeddings for input text.
        
        Args:
            text (Union[str, List[str]]): Input text or list of texts
            
        Returns:
            np.ndarray: Generated embeddings
        """
        if isinstance(text, str):
            text = [self.preprocess_text(text)]
        else:
            text = [self.preprocess_text(t) for t in text]
            
        # Generate embeddings with proper parameters
        embeddings = self.model.encode(text)
        
        # Ensure correct shape
        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
            
        return embeddings
    
    def normalize_embeddings(self, embeddings: np.ndarray) -> np.ndarray:
        """Normalize the embeddings to unit length.
        
        Args:
            embeddings (np.ndarray): Input embeddings
            
        Returns:
            np.ndarray: Normalized embeddings
        """
        norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
        return embeddings / norms
    
    def compute_similarity(self, query_embedding: np.ndarray, 
                         database_embeddings: np.ndarray) -> np.ndarray:
        """Compute cosine similarity between query and database embeddings.
        
        Args:
            query_embedding (np.ndarray): Query embedding
            database_embeddings (np.ndarray): Database embeddings
            
        Returns:
            np.ndarray: Similarity scores
        """
        # Use cosine similarity for better matching
        normalized_query = self.normalize_embeddings(query_embedding)
        normalized_db = self.normalize_embeddings(database_embeddings)
        return np.dot(normalized_db, normalized_query.T).flatten() 