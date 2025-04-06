"""
Payment integration for the astrology platform
"""

import stripe
import streamlit as st
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Stripe
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Define payment plans
PLANS = {
    'starter': {
        'name': 'Starter',
        'price': 9.99,
        'price_id': 'price_starter',  # Replace with actual Stripe price ID
        'features': [
            'Daily Horoscope',
            'Basic Birth Chart',
            '7-Day Free Trial',
            'Community Access',
            'Email Support'
        ]
    },
    'premium': {
        'name': 'Premium',
        'price': 19.99,
        'price_id': 'price_premium',  # Replace with actual Stripe price ID
        'features': [
            'Everything in Starter',
            'Detailed Birth Chart',
            'Relationship Compatibility',
            'Priority Support',
            'Monthly Reading'
        ]
    },
    'pro': {
        'name': 'Pro',
        'price': 39.99,
        'price_id': 'price_pro',  # Replace with actual Stripe price ID
        'features': [
            'Everything in Premium',
            'Unlimited Readings',
            'Personal Astrologer',
            '24/7 Support',
            'Yearly Forecast'
        ]
    }
}

def create_checkout_session(plan_id):
    try:
        # Create Stripe checkout session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': PLANS[plan_id]['price_id'],
                'quantity': 1,
            }],
            mode='subscription',
            success_url=st.markdown(f"{st.get_option('server.baseUrlPath')}/success?session_id={{CHECKOUT_SESSION_ID}}"),
            cancel_url=st.markdown(f"{st.get_option('server.baseUrlPath')}/cancel"),
        )
        return session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None

def display_pricing_page():
    st.title("Choose Your Plan")
    st.write("Start your astrological journey today with our flexible plans")
    
    # Create three columns for pricing plans
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader(PLANS['starter']['name'])
        st.write(f"${PLANS['starter']['price']}/month")
        for feature in PLANS['starter']['features']:
            st.write(f"✓ {feature}")
        if st.button("Start Free Trial", key="starter"):
            checkout_url = create_checkout_session('starter')
            if checkout_url:
                st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
    
    with col2:
        st.subheader(PLANS['premium']['name'])
        st.write(f"${PLANS['premium']['price']}/month")
        for feature in PLANS['premium']['features']:
            st.write(f"✓ {feature}")
        if st.button("Start Free Trial", key="premium"):
            checkout_url = create_checkout_session('premium')
            if checkout_url:
                st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
    
    with col3:
        st.subheader(PLANS['pro']['name'])
        st.write(f"${PLANS['pro']['price']}/month")
        for feature in PLANS['pro']['features']:
            st.write(f"✓ {feature}")
        if st.button("Start Free Trial", key="pro"):
            checkout_url = create_checkout_session('pro')
            if checkout_url:
                st.markdown(f'<meta http-equiv="refresh" content="0;url={checkout_url}">', unsafe_allow_html=True)
    
    # FAQ Section
    st.markdown("---")
    st.subheader("Frequently Asked Questions")
    
    faqs = [
        {
            "question": "How does the free trial work?",
            "answer": "Start with a 7-day free trial. No credit card required. Cancel anytime during the trial period."
        },
        {
            "question": "Can I change my plan later?",
            "answer": "Yes, you can upgrade or downgrade your plan at any time. Changes will be reflected in your next billing cycle."
        },
        {
            "question": "What payment methods do you accept?",
            "answer": "We accept all major credit cards, PayPal, and Apple Pay."
        }
    ]
    
    for faq in faqs:
        with st.expander(faq["question"]):
            st.write(faq["answer"])
    
    # Money-back guarantee
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #f8f9fa; border-radius: 10px;'>
        <h3>30-Day Money-Back Guarantee</h3>
        <p>Not satisfied? Get a full refund within 30 days of your purchase.</p>
    </div>
    """, unsafe_allow_html=True)

def display_payment_success():
    st.title("Payment Successful! 🎉")
    st.write("Thank you for subscribing to our astrology platform.")
    st.write("You can now access all the features of your chosen plan.")
    st.button("Go to Dashboard", on_click=lambda: st.switch_page("pages/dashboard.py"))

def display_payment_cancel():
    st.title("Payment Cancelled")
    st.write("Your payment was cancelled. No charges were made.")
    st.write("Feel free to try again or contact our support team if you have any questions.")
    st.button("Return to Pricing", on_click=lambda: st.switch_page("pages/pricing.py")) 