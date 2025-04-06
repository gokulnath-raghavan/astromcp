import streamlit as st
import datetime
import os
from astro_mcp.core.calculator import AstroCalculator
from astro_mcp.core.interpreter import ContextualInterpreter
from astro_mcp.core.models import NatalChart

# Domain configuration
DOMAIN = "astrologycontext.in"
BASE_URL = f"https://{DOMAIN}"

st.set_page_config(
    page_title="Astrology Model Context Protocol",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom CSS for domain-specific styling
st.markdown(f"""
    <style>
    .main {{
        background-color: #f8f9fa;
    }}
    .stButton>button {{
        background-color: #6c5ce7;
        color: white;
        border-radius: 20px;
        padding: 10px 20px;
        border: none;
        transition: all 0.3s ease;
    }}
    .stButton>button:hover {{
        background-color: #5b4cc4;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }}
    .stMarkdown {{
        color: #2d3436;
    }}
    .css-1d391kg {{
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }}
    </style>
""", unsafe_allow_html=True)

st.title("✨ Astrology Model Context Protocol")
st.markdown(f"""
    This application provides a comprehensive framework for astrological analysis 
    with contextual interpretation through multiple lenses.
    
    Visit us at: [{DOMAIN}]({BASE_URL})
""")

# API Key Configuration
with st.sidebar:
    st.header("API Configuration")
    user_id = st.text_input(
        "User ID",
        value="639454",  # Your user ID
        help="Your AstrologyAPI User ID"
    )
    api_key = st.text_input(
        "API Key",
        value="0a2ba88ba63a2ca0cff8da7b6ed3a8616a8214ff",  # Your API key
        type="password",
        help="Your AstrologyAPI API Key"
    )
    
    if not user_id or not api_key:
        st.warning("""
            Please enter your AstrologyAPI credentials to continue.
            You can find these in your AstrologyAPI dashboard:
            1. User ID: 639454
            2. API Key: Your generated API key
        """)
        st.stop()

# Birth Information
with st.sidebar:
    st.header("Birth Information")
    birth_date = st.date_input("Birth Date", datetime.date(1990, 1, 1))
    birth_time = st.time_input("Birth Time", datetime.time(12, 0))
    latitude = st.number_input("Birth Latitude", value=0.0, step=0.1)
    longitude = st.number_input("Birth Longitude", value=0.0, step=0.1)
    timezone = st.text_input("Timezone (optional)", "UTC")
    
    include_contextual = st.checkbox("Include Contextual Analysis", value=True)
    
    if st.button("Generate Chart"):
        birth_datetime = datetime.datetime.combine(birth_date, birth_time)
        calculator = AstroCalculator(user_id, api_key)
        
        try:
            with st.spinner("Generating chart..."):
                chart = calculator.generate_natal_chart(
                    birth_datetime,
                    latitude,
                    longitude
                )
                
                # Store chart data in session state
                st.session_state['chart'] = chart
                st.session_state['birth_datetime'] = birth_datetime
                st.session_state['latitude'] = latitude
                st.session_state['longitude'] = longitude
                
                if include_contextual:
                    interpreter = ContextualInterpreter()
                    st.session_state['interpretation'] = interpreter.interpret_chart(chart)
                
                st.success("Chart generated successfully!")
        except Exception as e:
            st.error(f"Error generating chart: {str(e)}")
            st.stop()

# Main content area
if 'chart' in st.session_state:
    chart = st.session_state['chart']
    
    # Display birth details
    st.header("Birth Details")
    st.write(f"**Date**: {chart.birth_time.strftime('%Y-%m-%d')}")
    st.write(f"**Time**: {chart.birth_time.strftime('%H:%M')}")
    st.write(f"**Location**: {chart.birth_location['latitude']}°N, {chart.birth_location['longitude']}°E")
    
    # Display contextual analysis
    st.header("Contextual Analysis")
    st.subheader("Basic Interpretation")
    st.write("Based on the available data, here are some insights:")
    
    # Add some basic interpretations based on birth details
    if chart.additional_context:
        birth_details = chart.additional_context.get('birth_details', {})
        panchang = chart.additional_context.get('panchang', {})
        
        if birth_details:
            st.write("**Birth Time Analysis**:")
            hour = chart.birth_time.hour
            if 4 <= hour < 12:
                st.write("- Born during the morning hours, suggesting an active and energetic nature")
            elif 12 <= hour < 18:
                st.write("- Born during the afternoon, indicating a balanced and social personality")
            elif 18 <= hour < 22:
                st.write("- Born during the evening, suggesting a reflective and creative nature")
            else:
                st.write("- Born during the night, indicating an intuitive and self-reflective personality")
            
            # Add sunrise/sunset analysis from birth details
            sunrise = birth_details.get('sunrise', '')
            sunset = birth_details.get('sunset', '')
            if sunrise and sunset:
                st.write("\n**Day Length Analysis**:")
                st.write(f"- The day length was from {sunrise} to {sunset}, indicating a balanced exposure to both light and dark periods")
        
        if panchang:
            st.write("\n**Panchang Analysis**:")
            st.write(f"- Born on {panchang.get('day', '')}, suggesting a strong sense of purpose and leadership qualities")
            st.write(f"- The lunar day (Tithi) was {panchang.get('tithi', '')}, indicating a period of growth and development")
            st.write(f"- The Nakshatra was {panchang.get('nakshatra', '')}, suggesting unique talents and abilities")
            st.write(f"- The Yoga was {panchang.get('yog', '')}, indicating favorable conditions for success")
            st.write(f"- The Karan was {panchang.get('karan', '')}, suggesting a balanced approach to life")
    else:
        st.write("No additional context available for interpretation.")

# Add a footer
st.markdown("---")
st.markdown("""
    *This application is part of the Astrology Model Context Protocol framework.*
    *For more information, please refer to the documentation.*
""") 