from database import AstrologyDB
from astrological_data import ALL_INTERPRETATIONS
import os
from pathlib import Path

def main():
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Initialize database with persistence
    db = AstrologyDB(persist_dir=str(data_dir))
    
    # Add all interpretations to the database
    for interpretation in ALL_INTERPRETATIONS:
        db.add_interpretation(
            text=interpretation["text"],
            metadata=interpretation["metadata"]
        )
    
    print(f"Added {len(ALL_INTERPRETATIONS)} interpretations to the database")
    
    # Test some searches
    test_queries = [
        ("What does it mean to have Sun in Aries?", None, None, None),
        ("Tell me about Moon in Cancer", None, "Moon", None),
        ("What are the characteristics of Venus in Taurus?", None, "Venus", "Taurus"),
        ("Explain the First House", "House", None, None),
        ("What does Sun conjunct Moon mean?", "Planetary Aspect", None, None)
    ]
    
    print("\nTesting searches:")
    print("-" * 50)
    
    for query, category, planet, sign in test_queries:
        print(f"\nQuery: {query}")
        results = db.search(query, k=3, category=category, planet=planet, sign=sign)
        
        for text, score, metadata in results:
            print(f"\nScore: {score:.3f}")
            print(f"Text: {text}")
            print(f"Metadata: {metadata}")
        print("-" * 50)
    
    # Test metadata search
    print("\nTesting metadata search:")
    print("-" * 50)
    
    metadata_filters = {
        "category": "Sun Sign",
        "element": "Fire"
    }
    
    results = db.search_by_metadata(metadata_filters, k=3)
    for text, score, metadata in results:
        print(f"\nScore: {score:.3f}")
        print(f"Text: {text}")
        print(f"Metadata: {metadata}")
    print("-" * 50)

if __name__ == "__main__":
    main() 