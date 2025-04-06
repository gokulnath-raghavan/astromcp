import streamlit as st
from database import AstrologyDB
from bot import AstrologyBot
from payments import display_pricing_page, display_payment_success, display_payment_cancel
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
from pathlib import Path

# Load environment variables
load_dotenv()

# Set page config
st.set_page_config(
    page_title="Astrology Platform",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #6c5ce7;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #5b4cc4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stMarkdown {
        color: #2d3436;
    }
    .css-1d391kg {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .feature-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .astrologer-card {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        text-align: center;
    }
    .astrologer-card img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        object-fit: cover;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Sample astrologer data (in a real app, this would come from a database)
ASTROLOGERS = [
    {
        "id": 1,
        "name": "Dr. Sarah Johnson",
        "specialty": "Vedic Astrology",
        "experience": "15 years",
        "rating": 4.8,
        "image": "https://randomuser.me/api/portraits/women/1.jpg",
        "videos": [
            {
                "title": "Understanding Your Birth Chart",
                "url": "https://example.com/video1",
                "thumbnail": "https://picsum.photos/300/200"
            },
            {
                "title": "Planetary Transits 2024",
                "url": "https://example.com/video2",
                "thumbnail": "https://picsum.photos/300/200"
            }
        ],
        "price_per_hour": 100
    },
    {
        "id": 2,
        "name": "Rajesh Kumar",
        "specialty": "Western Astrology",
        "experience": "12 years",
        "rating": 4.9,
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "videos": [
            {
                "title": "Zodiac Sign Compatibility",
                "url": "https://example.com/video3",
                "thumbnail": "https://picsum.photos/300/200"
            }
        ],
        "price_per_hour": 80
    }
]

# Initialize the database and bot
@st.cache_resource
def initialize_bot():
    db = AstrologyDB()
    bot = AstrologyBot(db)
    
    # Load comprehensive astrological interpretations
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
    
    return bot

def display_astrologer_profile(astrologer):
    st.header(f"✨ {astrologer['name']}")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(astrologer['image'], width=200)
        st.markdown(f"**Specialty:** {astrologer['specialty']}")
        st.markdown(f"**Experience:** {astrologer['experience']}")
        st.markdown(f"**Rating:** ⭐ {astrologer['rating']}")
        st.markdown(f"**Price:** ${astrologer['price_per_hour']}/hour")
    
    with col2:
        st.subheader("Videos")
        for video in astrologer['videos']:
            st.image(video['thumbnail'], width=300)
            st.markdown(f"**{video['title']}**")
            if st.button("Watch Video", key=f"watch_{video['title']}"):
                st.video(video['url'])
        
        st.subheader("Book a Session")
        session_date = st.date_input(
            "Select Date",
            min_value=datetime.now().date(),
            max_value=datetime.now().date() + timedelta(days=30),
            key=f"date_{astrologer['id']}"
        )
        session_time = st.time_input("Select Time", key=f"time_{astrologer['id']}")
        session_duration = st.select_slider(
            "Session Duration",
            options=[30, 60, 90, 120],
            value=60,
            format_func=lambda x: f"{x} minutes",
            key=f"duration_{astrologer['id']}"
        )
        
        if st.button("Book Now", key=f"book_{astrologer['id']}"):
            total_price = (session_duration / 60) * astrologer['price_per_hour']
            st.info(f"Total Price: ${total_price}")
            # Here you would integrate with a payment gateway
            if st.button("Proceed to Payment", key=f"payment_{astrologer['id']}"):
                st.success("Booking successful! You will be redirected to the video call shortly.")
                # Here you would integrate with a video calling service

def main():
    # Sidebar
    with st.sidebar:
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <h1 style='color: #6c5ce7;'>✨ Astrology Platform</h1>
                <p style='color: #636e72;'>Your journey to self-discovery</p>
            </div>
        """, unsafe_allow_html=True)
        
        page = st.radio(
            "Navigation",
            ["Home", "Search", "Pricing", "Astrologers", "Dashboard", "Contact"],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        st.markdown("""
            <div style='text-align: center; padding: 20px;'>
                <p style='color: #636e72;'>Need help?</p>
                <p style='color: #6c5ce7;'>support@astrology.com</p>
            </div>
        """, unsafe_allow_html=True)

    # Main content
    if page == "Home":
        # Hero section
        st.markdown("""
            <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #6c5ce7 0%, #a8a4e6 100%); border-radius: 15px; color: white;'>
                <h1 style='font-size: 3em; margin-bottom: 20px;'>Discover Your Destiny</h1>
                <p style='font-size: 1.2em;'>Get personalized astrological insights and guidance from expert astrologers</p>
            </div>
        """, unsafe_allow_html=True)

        # Features section
        st.markdown("### 🌟 Our Features")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class='feature-card'>
                    <h3>Personalized Readings</h3>
                    <p>Get detailed insights based on your unique birth chart</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='feature-card'>
                    <h3>Expert Astrologers</h3>
                    <p>Connect with experienced professionals</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class='feature-card'>
                    <h3>Daily Horoscopes</h3>
                    <p>Stay updated with your daily astrological guidance</p>
                </div>
            """, unsafe_allow_html=True)

        # Featured Astrologers
        st.markdown("### 👨‍💼 Featured Astrologers")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/men/1.jpg' alt='Astrologer 1'>
                    <h3>Dr. James Wilson</h3>
                    <p>Vedic Astrology Expert</p>
                    <p>⭐ 4.9/5</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/women/1.jpg' alt='Astrologer 2'>
                    <h3>Sarah Chen</h3>
                    <p>Western Astrology Specialist</p>
                    <p>⭐ 4.8/5</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/men/2.jpg' alt='Astrologer 3'>
                    <h3>Michael Patel</h3>
                    <p>Numerology Expert</p>
                    <p>⭐ 4.7/5</p>
                </div>
            """, unsafe_allow_html=True)

        # Call to Action
        st.markdown("""
            <div style='text-align: center; padding: 40px 20px; background-color: #f8f9fa; border-radius: 15px; margin-top: 40px;'>
                <h2>Ready to Begin Your Journey?</h2>
                <p>Choose a subscription plan and get started today</p>
                <a href='#pricing'><button style='background-color: #6c5ce7; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;'>View Plans</button></a>
            </div>
        """, unsafe_allow_html=True)

    elif page == "Search":
        st.markdown("""
            <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #6c5ce7 0%, #a8a4e6 100%); border-radius: 15px; color: white; margin-bottom: 40px;'>
                <h1 style='font-size: 2.5em; margin-bottom: 20px;'>🔍 Astrological Search</h1>
                <p style='font-size: 1.2em;'>Search our comprehensive database of astrological interpretations</p>
            </div>
        """, unsafe_allow_html=True)

        # Search interface
        col1, col2 = st.columns([3, 1])
        
        with col1:
            query = st.text_input("Enter your astrological question", placeholder="e.g., What does it mean to have Sun in Leo?")
        
        with col2:
            category = st.selectbox(
                "Category",
                ["All", "Sun Sign", "Moon Sign", "Planetary Aspect", "House", "General"]
            )
        
        if query:
            # Initialize bot if not already done
            if 'bot' not in st.session_state:
                st.session_state.bot = initialize_bot()
            
            # Get search results
            results = st.session_state.bot.get_relevant_interpretations(query, k=5)
            
            if results:
                st.markdown("### 📚 Search Results")
                for result in results:
                    with st.expander(f"Score: {result['score']:.2f}"):
                        st.markdown(f"**Interpretation:** {result['text']}")
                        if result['metadata']:
                            st.markdown("**Details:**")
                            for key, value in result['metadata'].items():
                                st.markdown(f"- {key}: {value}")
            else:
                st.info("No results found. Try rephrasing your question or selecting a different category.")
        
        # Example queries
        st.markdown("### 💡 Example Queries")
        example_queries = [
            "What does it mean to have Mars in Leo?",
            "Tell me about Moon in Cancer",
            "What are the characteristics of Venus in Taurus?",
            "Explain the First House",
            "What does Sun conjunct Moon mean?"
        ]
        
        for query in example_queries:
            if st.button(query):
                st.session_state.query = query
                st.experimental_rerun()
    
    elif page == "Pricing":
        display_pricing_page()
    
    elif page == "Astrologers":
        st.markdown("### 👨‍💼 Our Expert Astrologers")
        st.markdown("""
            <div style='display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;'>
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/men/1.jpg' alt='Astrologer 1'>
                    <h3>Dr. James Wilson</h3>
                    <p>Vedic Astrology Expert</p>
                    <p>⭐ 4.9/5</p>
                    <p>15+ years of experience</p>
                    <button style='background-color: #6c5ce7; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;'>Book Session</button>
                </div>
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/women/1.jpg' alt='Astrologer 2'>
                    <h3>Sarah Chen</h3>
                    <p>Western Astrology Specialist</p>
                    <p>⭐ 4.8/5</p>
                    <p>12+ years of experience</p>
                    <button style='background-color: #6c5ce7; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;'>Book Session</button>
                </div>
                <div class='astrologer-card'>
                    <img src='https://randomuser.me/api/portraits/men/2.jpg' alt='Astrologer 3'>
                    <h3>Michael Patel</h3>
                    <p>Numerology Expert</p>
                    <p>⭐ 4.7/5</p>
                    <p>10+ years of experience</p>
                    <button style='background-color: #6c5ce7; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;'>Book Session</button>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    elif page == "Dashboard":
        st.markdown("### 📊 Your Dashboard")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                <div style='background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <h3>Your Profile</h3>
                    <p>Name: John Doe</p>
                    <p>Email: john@example.com</p>
                    <p>Subscription: Premium</p>
                    <p>Next Reading: March 25, 2024</p>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div style='background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                    <h3>Recent Readings</h3>
                    <ul>
                        <li>Birth Chart Analysis - March 20, 2024</li>
                        <li>Career Horoscope - March 15, 2024</li>
                        <li>Relationship Reading - March 10, 2024</li>
                    </ul>
                </div>
            """, unsafe_allow_html=True)
    
    elif page == "Contact":
        st.markdown("### 📞 Contact Us")
        st.markdown("""
            <div style='background-color: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                <h3>Get in Touch</h3>
                <p>Have questions? We're here to help!</p>
                <form>
                    <div style='margin-bottom: 20px;'>
                        <label>Name</label>
                        <input type='text' style='width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>
                    </div>
                    <div style='margin-bottom: 20px;'>
                        <label>Email</label>
                        <input type='email' style='width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px;'>
                    </div>
                    <div style='margin-bottom: 20px;'>
                        <label>Message</label>
                        <textarea style='width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; height: 150px;'></textarea>
                    </div>
                    <button style='background-color: #6c5ce7; color: white; border: none; padding: 10px 20px; border-radius: 20px; cursor: pointer;'>Send Message</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        st.error("Error: OPENAI_API_KEY not found in .env file")
        st.info("Please add your OpenAI API key to the .env file")
    else:
        main() 