from database import AstrologyDB
from bot import AstrologyBot

def main():
    # Initialize the database
    db = AstrologyDB()
    
    # Add some sample interpretations
    sample_data = [
        {
            "text": "When the Sun is in Leo, it brings out leadership qualities and creative expression. This is a time for self-confidence and taking center stage.",
            "metadata": {"planet": "Sun", "sign": "Leo"}
        },
        {
            "text": "A Mercury in Gemini placement enhances communication skills and intellectual curiosity. It's an excellent time for learning and networking.",
            "metadata": {"planet": "Mercury", "sign": "Gemini"}
        },
        {
            "text": "Venus in Taurus brings stability to relationships and an appreciation for beauty and luxury. This placement favors long-term commitments.",
            "metadata": {"planet": "Venus", "sign": "Taurus"}
        }
    ]
    
    # Add interpretations to the database
    for item in sample_data:
        db.add_interpretation(item["text"], item["metadata"])
    
    # Initialize the bot
    bot = AstrologyBot(db)
    
    # Test queries
    test_queries = [
        "What does it mean to have the Sun in Leo?",
        "How does Mercury in Gemini affect communication?",
        "Tell me about Venus in Taurus relationships"
    ]
    
    # Process each query
    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        response = bot.process_query(query)
        print(f"Response: {response}")
        print("-" * 50)

if __name__ == "__main__":
    main() 