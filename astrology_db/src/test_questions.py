from database import AstrologyDB
from bot import AstrologyBot

def initialize_database():
    db = AstrologyDB()
    
    # Add comprehensive astrological interpretations
    interpretations = [
        # Sun Sign Interpretations
        "Sun in Aries represents leadership, initiative, and a pioneering spirit. This placement indicates strong willpower and natural confidence.",
        "Sun in Taurus shows determination, practicality, and appreciation for beauty. This placement brings stability and material focus.",
        "Sun in Gemini indicates adaptability, communication skills, and intellectual curiosity. This placement brings versatility and social charm.",
        "Sun in Cancer represents emotional depth, nurturing instincts, and strong intuition. This placement shows deep family ties and protective nature.",
        "Sun in Leo demonstrates creativity, leadership, and dramatic self-expression. This placement brings natural charisma and desire for recognition.",
        "Sun in Virgo shows analytical thinking, attention to detail, and service-oriented nature. This placement brings practical skills and perfectionism.",
        "Sun in Libra represents diplomacy, harmony-seeking, and artistic appreciation. This placement shows strong relationship focus and aesthetic sense.",
        "Sun in Scorpio indicates intensity, emotional depth, and transformative power. This placement brings psychological insight and magnetic presence.",
        "Sun in Sagittarius shows optimism, philosophical thinking, and adventurous spirit. This placement brings expansion and truth-seeking nature.",
        "Sun in Capricorn represents ambition, responsibility, and practical achievement. This placement shows strong work ethic and long-term planning.",
        "Sun in Aquarius indicates innovation, humanitarian ideals, and unique perspective. This placement brings progressive thinking and social awareness.",
        "Sun in Pisces shows compassion, artistic talent, and spiritual awareness. This placement brings sensitivity and creative imagination.",
        
        # Moon Sign Interpretations
        "Moon in Aries shows emotional impulsiveness, independence, and quick reactions. This placement indicates strong emotional needs for freedom.",
        "Moon in Taurus represents emotional stability, comfort-seeking, and sensual nature. This placement shows strong attachment to security.",
        "Moon in Gemini indicates emotional versatility, intellectual stimulation, and social needs. This placement shows need for mental engagement.",
        "Moon in Cancer shows strong emotional sensitivity, nurturing instincts, and family focus. This placement represents deep emotional security needs.",
        "Moon in Leo demonstrates emotional expressiveness, pride, and need for recognition. This placement shows dramatic emotional nature.",
        "Moon in Virgo represents emotional practicality, service, and need for order. This placement shows analytical emotional approach.",
        "Moon in Libra shows emotional harmony-seeking, partnership needs, and aesthetic sensitivity. This placement indicates balance-seeking nature.",
        "Moon in Scorpio represents emotional intensity, depth, and transformative experiences. This placement shows powerful emotional nature.",
        "Moon in Sagittarius indicates emotional optimism, freedom-seeking, and philosophical outlook. This placement shows adventurous emotional nature.",
        "Moon in Capricorn shows emotional control, responsibility, and traditional values. This placement represents structured emotional approach.",
        "Moon in Aquarius represents emotional independence, innovation, and social consciousness. This placement shows unique emotional expression.",
        "Moon in Pisces indicates emotional sensitivity, compassion, and spiritual connection. This placement shows dreamy emotional nature.",
        
        # Planetary Aspects
        "Sun conjunct Moon represents harmony between conscious and unconscious self. This aspect shows integrated personality and emotional balance.",
        "Sun square Moon indicates tension between conscious and unconscious needs. This aspect shows internal conflict and growth opportunities.",
        "Sun trine Moon shows easy flow between conscious and unconscious expression. This aspect represents natural emotional harmony.",
        "Venus conjunct Mars represents strong romantic and sexual attraction. This aspect shows passionate relationships and creative energy.",
        "Jupiter square Saturn indicates tension between expansion and limitation. This aspect shows growth challenges and responsibility.",
        "Uranus conjunct Neptune represents innovative spiritual awareness. This aspect shows unique spiritual insights and revolutionary ideas.",
        
        # House Interpretations
        "First House represents self-image, personality, and physical appearance. This house shows how others see you and your approach to life.",
        "Second House indicates values, possessions, and self-worth. This house shows material resources and personal values.",
        "Third House represents communication, siblings, and short journeys. This house shows learning style and immediate environment.",
        "Fourth House shows home, family, and emotional foundation. This house represents roots and private life.",
        "Fifth House indicates creativity, romance, and children. This house shows self-expression and pleasure.",
        "Sixth House represents work, health, and daily routines. This house shows service and practical matters.",
        "Seventh House shows partnerships, marriage, and relationships. This house represents one-on-one connections.",
        "Eighth House indicates transformation, shared resources, and deep psychology. This house shows power and regeneration.",
        "Ninth House represents higher learning, travel, and philosophy. This house shows expansion and beliefs.",
        "Tenth House shows career, public status, and authority. This house represents achievement and reputation.",
        "Eleventh House indicates friends, groups, and future goals. This house shows social networks and aspirations.",
        "Twelfth House represents spirituality, secrets, and hidden matters. This house shows solitude and transcendence."
    ]
    
    # Add interpretations to the database with metadata
    for i, text in enumerate(interpretations):
        # Extract planet and sign from the text
        words = text.split()
        planet = words[0] if words[0] in ["Sun", "Moon", "Venus", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune", "Pluto", "Mercury"] else "N/A"
        sign = words[2] if len(words) > 2 and words[2] in ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"] else "N/A"
        
        metadata = {
            "planet": planet,
            "sign": sign,
            "index": i,
            "category": "Sun Sign" if planet == "Sun" else 
                      "Moon Sign" if planet == "Moon" else 
                      "Planetary Aspect" if "conjunct" in text or "square" in text or "trine" in text else 
                      "House" if "House" in text else "General"
        }
        db.add_interpretation(text, metadata)
    
    return db

def test_bot():
    # Initialize the database and bot
    db = initialize_database()
    bot = AstrologyBot(db)
    
    # Test questions covering different aspects of astrology
    test_questions = [
        # Sun Sign Questions
        "What does it mean to have the Sun in Leo?",
        "How does having Sun in Scorpio affect personality?",
        "Tell me about Sun in Aquarius characteristics",
        
        # Moon Sign Questions
        "What are the emotional characteristics of Moon in Cancer?",
        "How does Moon in Gemini affect emotional expression?",
        "What does Moon in Capricorn indicate about emotional nature?",
        
        # Planetary Aspect Questions
        "What does Sun conjunct Moon mean in a birth chart?",
        "How does Venus conjunct Mars affect relationships?",
        "What is the significance of Jupiter square Saturn?",
        
        # House Questions
        "What does the First House represent in astrology?",
        "How does the Seventh House influence relationships?",
        "What is the meaning of the Tenth House?",
        
        # Combined Questions
        "How does having Sun in Leo and Moon in Cancer affect personality?",
        "What does it mean to have Venus in Taurus in the Seventh House?",
        "How does Mars in Aries with Sun square Moon influence behavior?",
        
        # Specific Interpretation Questions
        "What are the career implications of having Sun in Capricorn?",
        "How does Moon in Pisces affect romantic relationships?",
        "What does Mercury in Gemini indicate about communication style?",
        
        # Birth Chart Questions
        "Interpret a birth chart for someone born on January 1, 1990 at 12:00 PM in New York",
        "What does having multiple planets in the same sign mean?",
        "How do house placements affect planetary positions?"
    ]
    
    print("Starting Astrology Bot Tests...\n")
    
    # Process each question
    for i, question in enumerate(test_questions, 1):
        print(f"\nTest Question {i}: {question}")
        print("-" * 50)
        try:
            response = bot.process_query(question)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error processing question: {str(e)}")
        print("-" * 50)

if __name__ == "__main__":
    test_bot() 