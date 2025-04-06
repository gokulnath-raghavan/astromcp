from database import AstrologyDB

def main():
    # Initialize the database
    db = AstrologyDB()
    
    # Example astrological interpretations
    interpretations = [
        "Sun in Aries represents leadership, initiative, and a pioneering spirit",
        "Moon in Cancer indicates emotional sensitivity and strong nurturing instincts",
        "Venus in Taurus shows appreciation for luxury, comfort, and sensual pleasures",
        "Mars in Leo demonstrates confidence, creativity, and a desire for recognition",
        "Jupiter in Sagittarius brings optimism, expansion, and philosophical growth",
        "Saturn in Capricorn represents discipline, responsibility, and long-term planning",
        "Uranus in Aquarius indicates innovation, independence, and humanitarian ideals",
        "Neptune in Pisces shows spiritual awareness, creativity, and compassion",
        "Pluto in Scorpio represents transformation, power, and deep psychological insight",
        "Mercury in Gemini indicates quick thinking, adaptability, and communication skills"
    ]
    
    # Add interpretations with metadata
    for i, text in enumerate(interpretations):
        metadata = {
            "planet": text.split()[0],
            "sign": text.split()[2],
            "index": i
        }
        db.add_interpretation(text, metadata)
    
    # Example searches
    queries = [
        "What does it mean to have Mars in Leo?",
        "Tell me about emotional sensitivity in astrology",
        "What are the characteristics of Mercury in Gemini?"
    ]
    
    print("\nSearching for astrological interpretations...")
    for query in queries:
        print(f"\nQuery: {query}")
        results = db.search(query, k=3)
        for text, score, metadata in results:
            print(f"\nScore: {score:.3f}")
            print(f"Interpretation: {text}")
            print(f"Metadata: {metadata}")

if __name__ == "__main__":
    main() 