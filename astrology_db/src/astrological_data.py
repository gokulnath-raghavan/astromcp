"""
Comprehensive astrological interpretations organized by categories.
"""

# Sun Sign Interpretations
SUN_SIGN_INTERPRETATIONS = [
    {
        "text": "Sun in Aries represents leadership, initiative, and a pioneering spirit. This placement indicates strong willpower and natural confidence. Aries Sun individuals are often trailblazers who inspire others with their courage and determination.",
        "metadata": {
            "planet": "Sun",
            "sign": "Aries",
            "category": "Sun Sign",
            "element": "Fire",
            "modality": "Cardinal",
            "ruling_planet": "Mars"
        }
    },
    {
        "text": "Sun in Taurus shows determination, practicality, and appreciation for beauty. This placement brings stability and material focus. Taurus Sun individuals are known for their reliability, patience, and strong connection to the physical world.",
        "metadata": {
            "planet": "Sun",
            "sign": "Taurus",
            "category": "Sun Sign",
            "element": "Earth",
            "modality": "Fixed",
            "ruling_planet": "Venus"
        }
    },
    {
        "text": "Sun in Gemini indicates adaptability, communication skills, and intellectual curiosity. This placement brings versatility and social charm. Gemini Sun individuals are known for their quick wit, learning ability, and natural talent for networking.",
        "metadata": {
            "planet": "Sun",
            "sign": "Gemini",
            "category": "Sun Sign",
            "element": "Air",
            "modality": "Mutable",
            "ruling_planet": "Mercury"
        }
    },
    {
        "text": "Sun in Cancer represents emotional depth, nurturing instincts, and strong intuition. This placement shows deep family ties and protective nature. Cancer Sun individuals are known for their emotional intelligence, caring nature, and strong connection to home and family.",
        "metadata": {
            "planet": "Sun",
            "sign": "Cancer",
            "category": "Sun Sign",
            "element": "Water",
            "modality": "Cardinal",
            "ruling_planet": "Moon"
        }
    }
]

# Moon Sign Interpretations
MOON_SIGN_INTERPRETATIONS = [
    {
        "text": "Moon in Cancer indicates emotional sensitivity and strong nurturing instincts. This placement shows deep emotional intelligence and a natural ability to care for others. Cancer Moon individuals are highly intuitive and deeply connected to their family and home.",
        "metadata": {
            "planet": "Moon",
            "sign": "Cancer",
            "category": "Moon Sign",
            "element": "Water",
            "modality": "Cardinal",
            "ruling_planet": "Moon"
        }
    },
    {
        "text": "Moon in Leo brings emotional warmth, creativity, and a desire for recognition. This placement indicates a need for emotional expression and dramatic flair. Leo Moon individuals are generous with their emotions and seek appreciation for their caring nature.",
        "metadata": {
            "planet": "Moon",
            "sign": "Leo",
            "category": "Moon Sign",
            "element": "Fire",
            "modality": "Fixed",
            "ruling_planet": "Sun"
        }
    },
    {
        "text": "Moon in Virgo shows emotional practicality and analytical thinking. This placement indicates a need for order and service to others. Virgo Moon individuals process emotions through practical problem-solving and find comfort in being helpful.",
        "metadata": {
            "planet": "Moon",
            "sign": "Virgo",
            "category": "Moon Sign",
            "element": "Earth",
            "modality": "Mutable",
            "ruling_planet": "Mercury"
        }
    },
    {
        "text": "Moon in Libra brings emotional harmony and relationship focus. This placement indicates a need for balance and partnership. Libra Moon individuals process emotions through relationships and seek peace and beauty in their emotional environment.",
        "metadata": {
            "planet": "Moon",
            "sign": "Libra",
            "category": "Moon Sign",
            "element": "Air",
            "modality": "Cardinal",
            "ruling_planet": "Venus"
        }
    }
]

# Planetary Aspects
PLANETARY_ASPECTS = [
    {
        "text": "Sun conjunct Moon represents a strong alignment between conscious and unconscious drives. This aspect indicates emotional harmony and clear self-expression. Individuals with this aspect often have a strong sense of self and clear emotional awareness.",
        "metadata": {
            "planet1": "Sun",
            "planet2": "Moon",
            "aspect": "conjunct",
            "category": "Planetary Aspect",
            "orb": "0-10 degrees"
        }
    },
    {
        "text": "Venus square Mars indicates tension between love and desire. This aspect often brings passionate relationships but may also indicate challenges in balancing romance and physical attraction. Individuals with this aspect may experience internal conflicts between their values and desires.",
        "metadata": {
            "planet1": "Venus",
            "planet2": "Mars",
            "aspect": "square",
            "category": "Planetary Aspect",
            "orb": "0-8 degrees"
        }
    },
    {
        "text": "Jupiter trine Saturn represents a harmonious balance between expansion and limitation. This aspect indicates good judgment and the ability to achieve long-term goals. Individuals with this aspect often have a natural talent for planning and execution.",
        "metadata": {
            "planet1": "Jupiter",
            "planet2": "Saturn",
            "aspect": "trine",
            "category": "Planetary Aspect",
            "orb": "0-8 degrees"
        }
    },
    {
        "text": "Mercury opposite Neptune can indicate confusion between reality and imagination. This aspect often brings creative thinking but may also lead to misunderstandings. Individuals with this aspect may need to work on grounding their thoughts in reality.",
        "metadata": {
            "planet1": "Mercury",
            "planet2": "Neptune",
            "aspect": "opposite",
            "category": "Planetary Aspect",
            "orb": "0-8 degrees"
        }
    }
]

# House Interpretations
HOUSE_INTERPRETATIONS = [
    {
        "text": "First House represents the self, personality, and physical appearance. This house shows how you present yourself to the world and your approach to new beginnings. Planets in the First House strongly influence your personality and life path.",
        "metadata": {
            "house": 1,
            "category": "House",
            "ruling_sign": "Aries",
            "ruling_planet": "Mars",
            "natural_house": "Angular"
        }
    },
    {
        "text": "Second House indicates values, possessions, and self-worth. This house shows your relationship with money, resources, and personal values. Planets in the Second House influence your financial matters and sense of self-worth.",
        "metadata": {
            "house": 2,
            "category": "House",
            "ruling_sign": "Taurus",
            "ruling_planet": "Venus",
            "natural_house": "Succedent"
        }
    },
    {
        "text": "Third House represents communication, siblings, and short-distance travel. This house shows your learning style and how you process information. Planets in the Third House influence your communication abilities and relationships with siblings.",
        "metadata": {
            "house": 3,
            "category": "House",
            "ruling_sign": "Gemini",
            "ruling_planet": "Mercury",
            "natural_house": "Cadent"
        }
    },
    {
        "text": "Fourth House indicates home, family, and emotional foundation. This house shows your roots and sense of security. Planets in the Fourth House influence your home life, family relationships, and emotional well-being.",
        "metadata": {
            "house": 4,
            "category": "House",
            "ruling_sign": "Cancer",
            "ruling_planet": "Moon",
            "natural_house": "Angular"
        }
    }
]

# Combine all interpretations
ALL_INTERPRETATIONS = (
    SUN_SIGN_INTERPRETATIONS +
    MOON_SIGN_INTERPRETATIONS +
    PLANETARY_ASPECTS +
    HOUSE_INTERPRETATIONS
) 